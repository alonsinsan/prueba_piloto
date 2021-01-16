# Create pilot test  
Given a design matrix, generates an experimental group that preserves features amongst the control and experimental group using Principal Component Analysis.  
* Design matrix should have id_column and features ONLY, passing other columns will affect the construction of the experimental group.
* Variables
1. n_components: number of components to use in principal components transformation.  
DEFAULT: 2
2. size: size for the experimental group, must be bigger than 4**n_components.  
DEFAULT: 100
3. path: path for he design matrix, design matrix should be in csv.  
DEFAULT: /pfs/pilot_test/dmat.csv
4. id_column: name for the id_column in design matrix.  
DEFAULT: pkcolocadora
5. group: in case design matrix should be filtered for a specific group.  
DEFAULT: 5  

## build
```
docker build -t pilot_test .
```

## run
```
docker run -it --rm -v /pfs/pilot_test/:/pfs/pilot_test/ -v /pfs/out:/pfs/out pilot_test python /home/jovyan/work/create_pilot_test.py  --n_components 2 --size 100 --path /pfs/pilot_test/dmat.csv --id_column pkcolocadora --group 5
```
