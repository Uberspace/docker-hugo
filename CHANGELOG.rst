=========
Changelog
=========

.. _Changelog_v0.5.1:

v0.5.1
======

.. _Changelog_v0.5.1_Added Features:

Added Features
--------------

- Added ``pipenv`` configuration for *development tools* (``bumpversion`` and ``reno``).


.. _Changelog_v0.5.1_Updates:

Updates
-------

- We now document the available *Docker tags* in the README.


.. _Changelog_v0.5.1_Fixes:

Fixes
-----

- Fixed the repo URL in the CI example in the README.


.. _Changelog_v0.5.0:

v0.5.0
======

.. _Changelog_v0.5.0_Added Features:

Added Features
--------------

- Support for configuration directories by *Hugo*.

- Added ``git`` to the image, to support *git* stats in *Hugo*.


.. _Changelog_v0.5.0_Changes:

Changes
-------

- Generate CHANGELOG with ``reno``.


.. _Changelog_v0.5.0_Updates:

Updates
-------

- Update *HUGO* to ``0.54.0`` (new defaut version too).


.. _Changelog_v0.4.0:

v0.4.0
======

.. _Changelog_v0.4.0_Added Features:

Added Features
--------------

- Use *Gitalab CI* to build the image.


.. _Changelog_v0.4.0_Removed:

Removed
-------

- Removed *development tools* from the repo.


.. _Changelog_v0.3.0:

v0.3.0
======

.. _Changelog_v0.3.0_Changes:

Changes
-------

- Container runs as ``root`` from ``/`` over ``/site`` to ``/public``.


.. _Changelog_v0.3.0_Updates:

Updates
-------

- Update *development tools*.


.. _Changelog_v0.3.0_Removed:

Removed
-------

- Removed links from ``/home/hugo/{input,output}`` → ``/{input,output}``.

- Removed ``.gitlab-ci.yaml`` for now.


.. _Changelog_v0.3.0_Known Issues:

Known Issues
------------

- Disabled *Gitlab CI* beacause of missing Docker runners.


.. _Changelog_v0.2.0:

v0.2.0
======

.. _Changelog_v0.2.0_Added Features:

Added Features
--------------

- Added TLS **ca-certificates** to image.


.. _Changelog_v0.1.0:

v0.1.0
======

.. _Changelog_v0.1.0_Summary:

Summary
-------

Initial version, pretty much _wip_.
