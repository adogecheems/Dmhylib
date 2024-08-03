from setuptools import setup


def requirements():
    with open("requirements.txt", 't') as f:
        return [req.strip() for req in f.readlines()]


setup(
    name='Dmhylib',  # 包名称
    packages=['src'],  # 需要处理的包目录
    version='0.0.1',  # 版本
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python', 'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'
    ],
    install_requires=requirements(),
    entry_points={'console_scripts': ['pmm=pimm.pimm_module:main']},
    package_data={'': ['*.json']},
    auth='adogecheems',  # 作者
    author_email='adogecheems@outlook.com',  # 作者邮箱
    description='',  # 介绍
    long_description=long_description,  # 长介绍，在pypi项目页显示
    long_description_content_type='text/markdown',  # 长介绍使用的类型，我使用的是md
    url='https://github.com/adogecheems/Dmhylib/',  # 包主页，一般是github项目主页
    license='GPL -v3',  # 协议
    keywords='dmhy automatic search'
)  # 关键字 搜索用
