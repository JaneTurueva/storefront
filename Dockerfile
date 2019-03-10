FROM python:3

# Create virtualenv
RUN pip3 install virtualenv
RUN virtualenv -p python3.7 /usr/share/python3/app

# Install all required modules into virtualenv
ADD requirements.txt /tmp/
RUN /usr/share/python3/app/bin/pip install -Ur /tmp/requirements.txt

# Install storefront source distribution to virtualenv
ADD dist/ /tmp/app/
RUN /usr/share/python3/app/bin/pip install /tmp/app/*

# Make storefront executables available from command line
RUN ln -snf /usr/share/python3/app/bin/storefront-api /usr/bin/storefront-api
RUN ln -snf /usr/share/python3/app/bin/storefront-db /usr/bin/storefront-db

# Default command
CMD ["storefront-api"]