from connectors import NetControllerJob, NetControllerConnector
from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect

class VCenterConnector(NetControllerConnector):
    def __init__(self):
        self._service_instance = None
        self._properties = {
            "address": "127.0.0.1",
            "port": 0,
            "username": "",
            "password": "",
            "monkey_template_name": "",
            "monkey_vm_info": {
                "name":   "Monkey Test",
                "datacenter_name":   "",
                "vm_folder":   "",
                "datastore_name":   "",
                "cluster_name":   "",
                "resource_pool":   ""
            }
        }
        self._cache = {
            "vlans" : []
        }

    def connect(self):
        import ssl
        try:
            self._service_instance = SmartConnect(host=self._properties["address"],
                                                  port=self._properties["port"],
                                                  user=self._properties["username"],
                                                  pwd=self._properties["password"])
        except ssl.SSLError:
            # some organizations use self-signed certificates...
            gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
            self._service_instance = SmartConnect(host=self._properties["address"],
                                                  port=self._properties["port"],
                                                  user=self._properties["username"],
                                                  pwd=self._properties["password"],
                                                  sslContext=gcontext)

    def is_connected(self):
        if (self._service_instance == None):
            return False
        try:
            self._service_instance.serverClock
        except vim.fault.NotAuthenticated, e:
            return False

    def get_vlans_list(self):
        if not self.is_connected():
            self.connect()
        if self._cache and self._cache.has_key("vlans") and self._cache["vlans"]:
            return self._cache["vlans"]
        vcontent = self._service_instance.RetrieveContent()  # get updated vsphare state
        vimtype = [vim.Network]
        objview = vcontent.viewManager.CreateContainerView(vcontent.rootFolder, vimtype, True)
        self._cache["vlans"] = [x.name for x in objview.view]
        objview.Destroy()
        return self._cache["vlans"]

    def get_entities_on_vlan(self, vlanid):
        return []

    def deploy_monkey(self, vm_name):
        if not self._properties["monkey_template_name"]:
            raise Exception("Monkey template not configured")

        if not self.is_connected():
            self.connect()

        vcontent = self._service_instance.RetrieveContent()  # get updated vsphare state
        monkey_template = self._get_obj(vcontent, [vim.VirtualMachine], self._properties["monkey_template_name"])
        if not monkey_template:
            raise Exception("Monkey template not found")

        self.log("Cloning vm: (%s -> %s)" % (monkey_template, vm_name))
        monkey_vm = self._clone_vm(vcontent, monkey_template, vm_name)
        if not monkey_vm:
            raise Exception("Error deploying monkey VM")
        self.log("Finished cloning")

        return monkey_vm

    def set_network(self, vm_obj, vlan_name):
        if not self.is_connected():
            self.connect()
        vcontent = self._service_instance.RetrieveContent()  # get updated vsphare state
        dvs_pg = self._get_obj(vcontent, [vim.dvs.DistributedVirtualPortgroup], vlan_name)
        nic = self._get_vm_nic(vm_obj)
        virtual_nic_spec = self._create_nic_spec(nic, dvs_pg)
        dev_changes = [virtual_nic_spec]
        spec = vim.vm.ConfigSpec()
        spec.deviceChange = dev_changes
        task = vm_obj.ReconfigVM_Task(spec=spec)
        return self._wait_for_task(task)

    def power_on(self, vm_obj):
        task = vm_obj.PowerOnVM_Task()
        return self._wait_for_task(task)

    def disconnect(self):
        Disconnect(self._service_instance)
        self._service_instance = None

    def __del__(self):
        if self._service_instance:
            self.disconnect()

    def _get_vm_nic(self, vm_obj):
        for dev in vm_obj.config.hardware.device:
            if isinstance(dev, vim.vm.device.VirtualEthernetCard):
                return dev
        return None

    def _create_nic_spec(self, virtual_nic_device, dvs_pg):
        virtual_nic_spec = vim.vm.device.VirtualDeviceSpec()
        virtual_nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
        virtual_nic_spec.device = virtual_nic_device
        virtual_nic_spec.device.key = virtual_nic_device.key
        virtual_nic_spec.device.macAddress = virtual_nic_device.macAddress
        virtual_nic_spec.device.wakeOnLanEnabled = virtual_nic_device.wakeOnLanEnabled

        virtual_nic_spec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
        virtual_nic_spec.device.connectable.startConnected = True
        virtual_nic_spec.device.connectable.connected = True
        virtual_nic_spec.device.connectable.allowGuestControl = True

        # configure port connection object on the requested dvs port group
        dvs_port_connection = vim.dvs.PortConnection()
        dvs_port_connection.portgroupKey = dvs_pg.key
        dvs_port_connection.switchUuid = dvs_pg.config.distributedVirtualSwitch.uuid

        # assign port to device
        virtual_nic_spec.device.backing = vim.vm.device.VirtualEthernetCard.DistributedVirtualPortBackingInfo()
        virtual_nic_spec.device.backing.port = dvs_port_connection

        return virtual_nic_spec

    def _clone_vm(self, vcontent, vm, name):

        # get vm target folder
        if self._properties["monkey_vm_info"]["vm_folder"]:
            destfolder = self._get_obj(vcontent, [vim.Folder], self._properties["monkey_vm_info"]["vm_folder"])
        else:
            datacenter = self._get_obj(vcontent, [vim.Datacenter], self._properties["monkey_vm_info"]["datacenter_name"])
            destfolder = datacenter.vmFolder

        # get vm target datastore
        if self._properties["monkey_vm_info"]["datacenter_name"]:
            datastore = self._get_obj(vcontent, [vim.Datastore], self._properties["monkey_vm_info"]["datacenter_name"])
        else:
            datastore = self._get_obj(vcontent, [vim.Datastore], vm.datastore[0].info.name)

        # get vm target resource pool
        if self._properties["monkey_vm_info"]["resource_pool"]:
            resource_pool = self._get_obj(vcontent, [vim.ResourcePool], self._properties["monkey_vm_info"]["resource_pool"])
        else:
            cluster = self._get_obj(vcontent, [vim.ClusterComputeResource], self._properties["monkey_vm_info"]["cluster_name"])
            resource_pool = cluster.resourcePool

        # set relospec
        relospec = vim.vm.RelocateSpec()
        relospec.datastore = datastore
        relospec.pool = resource_pool

        clonespec = vim.vm.CloneSpec()
        clonespec.location = relospec

        self.log("Starting clone task with the following info: %s" % repr({"folder": destfolder, "name": name, "clonespec": clonespec}))

        task = vm.Clone(folder=destfolder, name=name, spec=clonespec)
        return self._wait_for_task(task)

    def _wait_for_task(self, task):
        """ wait for a vCenter task to finish """
        task_done = False
        while not task_done:
            if task.info.state == 'success':
                if task.info.result:
                    return task.info.result
                else:
                    return True

            if task.info.state == 'error':
                self.log("Error waiting for task: %s" % repr(task.info))
                return None
        if task.info.state == 'success':
            return task.info.result
        return None


    @staticmethod
    def _get_obj(content, vimtype, name):
        """
        Return an object by name, if name is None the
        first found object is returned
        """
        obj = None
        container = content.viewManager.CreateContainerView(
            content.rootFolder, vimtype, True)
        for c in container.view:
            if name:
                if c.name == name:
                    obj = c
                    break
            else:
                obj = c
                break

        return obj


class VCenterJob(NetControllerJob):
    connector_type = VCenterConnector
    _vm_obj = None
    _properties = {
        "vlan": "",
        "vm_name": "",
    }
    _enumerations = {
        "vlan": "get_vlans_list",
    }

    def run(self):
        if not self._connector:
            return False

        monkey_vm = self._connector.deploy_monkey(self._properties["vm_name"])
        if not monkey_vm:
            return False

        self._vm_obj = monkey_vm

        self.log("Setting vm network")
        if not self._connector.set_network(monkey_vm, self._properties["vlan"]):
            return False

        self.log("Powering on vm")
        if not self._connector.power_on(monkey_vm):
            return False

        return True

