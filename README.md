# Openshift Images

This repo contains images and configurations design to be run under Openshift Origin - www.openshift.org

## Ubuntu 16 Base Image


This image supports the following hooks:

* /hooks/entrypoint-pre.d/: Early in the entrypoint. Before we do anything.
* /hooks/entrypoint-run: Runs if CMD is not overridden. (ie, we are doing daemon-mode or spawns a default bash shell).
* /hooks/entrypoint-exec: Runs only if CMD is overridden. Runs just before we execute CMD.
* /hooks/supervisord-pre.d/: Just before we fire up supervisord.
* /hooks/supervisord-ready: Runned after we know that supervisord is ready. This hook is triggered from supervisord itself, when it fires the SUPERVISOR_STATE_CHANGE_RUNNING event.




