##### Every time when we set up a new network on the server, we'd better set up a virtual environment first. The advantage of this is that you can play your project in this virtual environment, avoiding many problems arising from the environment of the system itself.

- Create a virtual environment：        conda create -n maskrcnn-benchmark python=3.6
- After creation：                     source activate maskrcnn-benchmark
- Uninstall the virtual environment： conda remove -n maskrcnn-benchmark --all

------
```
unzip  .tar.gz ：      tar -zxvf xx.tar.gz             

unzip  .tar.bz2 ：    tar -jxvf xx.tar.bz2
```



------
```
Add available Tsinghua source
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/

conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
```

