#!/bin/bash
# Setup script for the image recognition application

echo "画像認識アプリのセットアップを開始します..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "エラー: Python 3 がインストールされていません。"
    echo "https://www.python.org/downloads/ からインストールしてください。"
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Python バージョン: $python_version"

# Create virtual environment (optional)
read -p "仮想環境を作成しますか？ (y/n): " create_venv
if [[ $create_venv == "y" || $create_venv == "Y" ]]; then
    echo "仮想環境を作成中..."
    python3 -m venv venv
    
    # Activate virtual environment
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    echo "仮想環境を有効化しました。"
fi

# Install dependencies
echo "依存パッケージをインストール中..."
pip install -r requirements.txt

# Make scripts executable
chmod +x main.py cli.py demo.py run_tests.py

echo "セットアップが完了しました！"
echo ""
echo "アプリケーションを実行するには:"
echo "  - GUIアプリケーション: python main.py"
echo "  - コマンドラインインターフェース: python cli.py <画像ファイルのパス>"
echo "  - デモ: python demo.py"
echo ""
echo "テストを実行するには: python run_tests.py"