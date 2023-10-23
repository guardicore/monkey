const MachineView = (props) => {
    const {machine} = props
    return (
        <>
            <p>ID: {machine.id}</p>
            <p>Network Interfaces: {machine.network_interfaces}</p>
            <p>Is island: {String(machine.island)}</p>
            <p>Test field: {machine.test_field}</p>
        </>
    )
}

export default MachineView
