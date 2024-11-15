from setuptools import setup, find_packages

setup(
    name='dashboardtkinter',  # Cambia 'tu_proyecto' por el nombre de tu proyecto
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['data.json', 'imagenes/*.jpg', 'imagenes/*.png'],
    },
)
