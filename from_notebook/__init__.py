from ._import_hook import install as _install


# note: this does not do any mangling, so any notebook's filename will need to be changed to a valid python name
# it also (probably) won't be able to handle notebooks named "_import_hook" or "_install"
# (though if you have notebooks named shit like that, your issue is between you and your god)


_install()
