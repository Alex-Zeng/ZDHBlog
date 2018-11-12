from setuptools import find_packages, setup

setup(
    name="flask_zeng",
    version="1.0",
    packages=find_packages('.'),
    package_dir={'': '.'},  # 告诉distutils包都在src下
    package_data={
        # 任何包中含有.txt文件，都包含它
        '': ['*.txt'],
        # 包含app包templates文件夹中的 *.html文件
        'app': ['blues/admin/templates/*.html'],
    }

)

