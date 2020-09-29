"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.project.Project import Project


def test_create_project():
    project = Project('1', '2')
    assert isinstance(project, Project)

def test_create_project_with_semantic_constructor():
    id = str(uuid4())
    project = Project.createFrom(id=id, name='Prj1')
    assert isinstance(project, Project)
    assert project.id() == id
    assert project.name() == 'Prj1'
