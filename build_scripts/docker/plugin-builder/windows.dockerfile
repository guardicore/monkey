# Run with:
# docker build --platform=linux/amd64 --progress=plain -t plugin-builder:latest - < windows.dockerfile

# This dockerfile is based on tobix/pywine:3.11
# See:
# - https://github.com/webcomics/pywine
# - https://github.com/webcomics/wine-docker
# NOTE: tobix/pywine wine prefix location is stored in the WINEPREFIX env variable
# NOTE: It also installs the wine prefix with 777 permissions
FROM tobix/pywine:3.11

# Install git into the wine prefix
RUN cd /tmp && \
    umask 0 && \
    curl -Lo mingit.zip https://github.com/git-for-windows/git/releases/download/v2.45.1.windows.1/MinGit-2.45.1-64-bit.zip && \
    unzip mingit.zip -d $WINEPREFIX/drive_c/git && \
    rm mingit.zip

# Untested: Add user. The env variables are visible to all users
# RUN useradd -m -s /bin/bash wineuser
# USER wineuser

# Make git available in the wine prefix's PATH
ENV WINEPATH=C:\\git\\cmd
