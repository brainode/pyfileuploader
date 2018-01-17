# pyFileUploader

One page service written with flask and python 3.6 that allows you:
* Discover mapped folder and subfolders
* Upload files to selected folder
* Create a new folder at selected place
* Automatic transliterate russian file names
* Show used, free and total space on mapped folder

This service has docker image that can be [pulled](https://hub.docker.com/r/rusbaron/pyfileuploader/) using command
```bash
docker pull rusbaron/pyfileuploader
```
or you can build it by yourself using command:
```bash
docker build -t pyfileuploader .
```
in project directory.

To run docker image use this template:
```bash
docker run --name pyfileuploader -p YOURPORT:5000 \
           -v YOURPATH:/fileuploader/rootdir \
            -d --restart unless-stopped rusbaron/pyfileuploader
```
Or you can replace rusbaron/pyfileuploader to your builded image

TODO:
- [ ] Add logging actions to log file
- [ ] Implement unit test
- [ ] Integrate ci

Example: 
![Screenshot](https://i.imgur.com/oma7NAX.png)