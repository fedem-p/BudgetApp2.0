# Getting started

Build the docker file:

```docker build -t my-budget-image .```

where `python-dev latest` is a custom image with ubuntu and python installed.

and then run the container:

```docker run -it -v /home/fpuppo/workspace/budget-app/budget-app:/app my-budget-image```

attach vs code to the container and start developing!