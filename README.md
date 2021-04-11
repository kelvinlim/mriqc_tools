# mriqc_tools

Tools to parse output from fmriprep *desc-confounds_regressors.tsv file 
present in the target fmriprep output directory.


## to create a docker container
```
# run this command in the lnpireceiver directory
sudo docker build -t eyegazeqc .

```

## to run the container
```
# get the info on the container
sudo docker images | grep eyegazeqc
# to run the container on port 5003
# this makes it available at http://localhost:5003/posts 
sudo docker run -p 5003:5003 eyegazeqc

# there is a file x0-29.conf which is an apache config file
# which sets up reverseproxy
```