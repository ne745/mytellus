# 環境構築

## OS のアップデート
```
sudo apt update
sudo apt upgrade
```

## [Ubuntu 環境の Python](https://www.python.jp/install/ubuntu/index.html)
### ビルドツール・ライブラリのインストール
```
sudo apt install build-essential libbz2-dev libdb-dev \
  libreadline-dev libffi-dev libgdbm-dev liblzma-dev \
  libncursesw5-dev libsqlite3-dev libssl-dev \
  zlib1g-dev uuid-dev tk-dev
```

### ソースコードのダウンロード
[非公式Pythonダウンロードリンク](https://pythonlinks.python.jp/ja/index.html) からダウンロードして解凍
```
wget https://www.python.org/ftp/python/3.10.5/Python-3.10.5.tar.xz
tar xJf Python-3.10.5.tar.xz
```

### ビルド
```
cd Python-3.10.5
./configure
make
sudo make install
```

### 再起動
ビルドが終了すると Python のバージョンの変更を反映させるために Ubuntu を再起動する
```
sudo reboot now
```

### バージョンの確認
```
python3 --version
```
インストールされた Python のバージョンか確認する
```
which python3
```
/usr/local にインストールされているか確認する

### 不要ファイルの削除
```
sudo rm -rf Python-3.10.5
sudo rm Python-3.10.5.tar.xz
```

### エイリアスを追加
```
vim ~/.bashrc
```
.bashrc に下記を追記
``` .bashrc
alias python="python3"
alias pip="pip3"
```
変更を反映
```
source ~/.bashrc
```

### pip のアップグレード
```
python -m pip install --upgrade pip
```

### 仮想環境の構築
```
python -m venv venv
```
起動
```
source venv/bin/activate
```

## Jupyter Notebook の設定
### インストール
```
pip install notebook
```

### 設定
```
jupyter notebook --generate-config
```
config ファイルを編集
```
vim ~/.jupyter/jupyter_notebook_config.py
```
編集箇所
```
- # c.NotebookApp.ip = 'localhost'
+ c.NotebookApp.ip = '0.0.0.0'
- # c.NotebookApp.notebook_dir = ''
+ c.NotebookApp.notebook_dir = '/home/ubuntu/jupyter'
```

### パスワード設定　
```
jupyter notebook password
```
パスワードを入力する
config ファイルから暗号化されたパスワードをコピー
```
vim ~/.jupyter/jupyter_notebook_config.json
```
config ファイルに貼り付け
```
- # c.NotebookApp.password = ''
+ c.NotebookApp.password = 'paste_password'
```

### nbextensions のインストール
```
pip install jupyter-contrib-nbextensions
```
有効化
```
jupyter contrib nbextension install --user
jupyter nbextensions_configurator enable --user
```

### [jupyter-vim-binding](https://github.com/lambdalisue/jupyter-vim-binding) のインストール
```
# Create required directory in case (optional)
mkdir -p $(jupyter --data-dir)/nbextensions
# Clone the repository
cd $(jupyter --data-dir)/nbextensions
git clone https://github.com/lambdalisue/jupyter-vim-binding vim_binding
# Activate the extension
jupyter nbextension enable vim_binding/vim_binding
```

### Jupyter Notebook の起動
ポート転送設定
```
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8888
sudo iptables-save
```
起動コマンド
```
nohup jupyter notebook >> /home/ubuntu/working/jupyter/logs/jupyter.log 2>&1 &
```

## パッケージのインストール
```
pip install -r requirement.txt
```
もしくは
```
pip install numpy
pip install pandas
pip install matplotlib
pip install scikit-image
pip install requests
```