from gevent import monkey as gevent_monkey

# We need to monkeypatch before any other imports to
# make standard libraries compatible with gevent.
# http://www.gevent.org/api/gevent.monkey.html
gevent_monkey.patch_all()
