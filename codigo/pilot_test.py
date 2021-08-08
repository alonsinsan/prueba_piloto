import click
import os
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from random import sample

def validate_matrix(dmat, id_column):
    ids = dmat[id_column]
    aux = dmat.drop(id_column, axis =1)
    for col in aux.columns:
        if aux[col].dtype == 'object':
            aux = aux.drop(col, axis = 1)
            click.echo(f'Dropping {col}')
    aux = pd.concat([ids,aux], axis = 1)
    return aux

def transform_pca(dmat, n, id_column):
    # train and transform PCA (number of components)
    dmat.index = dmat[id_column]
    dmat = dmat.drop(id_column, axis = 1)
    click.echo(f'Using {dmat.columns.values} as features')
    pca = PCA(n_components = n)
    components = pd.DataFrame(data = pca.fit_transform(dmat), index = dmat.index)
    click.echo(f'Accumulative variance with {n} components: {np.sum(pca.explained_variance_ratio_)}')
    return components

def make_groups(X):
    # quantiles and make groups ()
    n = X.shape[1]
    division = X
    division['quantiles_group'] = ""
    for i in range(n):
        division.iloc[:,i] = pd.qcut(X.iloc[:,i], q = 4).astype(str)
        division['quantiles_group'] = division.quantiles_group + " & " + division.iloc[:,i]
    return division


def iterate_division(division, size, n_components):
    m = division.groupby('quantiles_group')[0].count()
    m = m[m>size/n_components].index
    experimental = []
    for group in m:
        empresarias = division[division.quantiles_group == group].index
        aux = sample(list(empresarias), round(size/len(m)))
        experimental.append(aux)
    division['indicador'] = 'control'
    experimental = [item for sublist in experimental for item in sublist]
    division.loc[division.index.isin(experimental), 'indicador'] = 'experimental'
    return division


@click.command()
@click.option('--n_components', default = 2, help = 'Number of components to use in PCA')
@click.option('--size', default = 100, help = 'Size of the experimental group, minimum equal to 4^n_components')
@click.option('--path', default = '/pfs/pilot_test/dmat.csv', help = 'Path for the design matrix file')
@click.option('--id_column', default = 'pkcolocadora', help = 'Id column name')
@click.option('--group', default = 5, help = 'Number of cluster group')
def create_experimental_group(n_components, size, path, id_column, group):
    """Script for creating an experimental group with a design matrix."""
    if (size >= 4**n_components):
        dmat = pd.read_csv(path)
        dmat = dmat[dmat.group == group].drop('group', axis=1)
        dmat = validate_matrix(dmat, id_column)
        components = transform_pca(dmat, n_components, id_column)
        division = make_groups(components)
        groups = iterate_division(division, size, n_components)
        groups.to_csv('/pfs/out/prueba_piloto.csv')
    else:
        click.echo(f'Error: minimum size should be {4**n_components}')


if __name__=="__main__":
    create_experimental_group()