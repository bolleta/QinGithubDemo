#!/usr/bin/env python3
"""
Demo script for the image recognition application.

This script demonstrates how to use the image recognition functionality
with a sample image.
"""

import os
import sys
import argparse
from image_recognition import recognize_image


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="画像認識デモ - サンプル画像でアプリをテストします"
    )
    
    parser.add_argument(
        "--image",
        help="認識する画像ファイルのパス (指定しない場合はサンプル画像を作成します)"
    )
    
    return parser.parse_args()


def create_sample_image():
    """
    Create a sample image for testing.
    
    Returns:
        str: Path to the created sample image.
    """
    try:
        from PIL import Image, ImageDraw
        
        # Create directory if it doesn't exist
        os.makedirs('samples', exist_ok=True)
        
        # Path for the sample image
        image_path = os.path.join('samples', 'sample.jpg')
        
        # Create a simple image (a white square with a black circle)
        img = Image.new('RGB', (300, 300), color='white')
        draw = ImageDraw.Draw(img)
        draw.ellipse((50, 50, 250, 250), fill='black')
        
        # Save the image
        img.save(image_path)
        print(f"サンプル画像を作成しました: {image_path}")
        return image_path
    
    except ImportError:
        print("エラー: PIL (Pillow) がインストールされていません。")
        print("pip install pillow を実行してインストールしてください。")
        sys.exit(1)
    except Exception as e:
        print(f"サンプル画像の作成中にエラーが発生しました: {str(e)}")
        sys.exit(1)


def main():
    """Main entry point for the demo script."""
    args = parse_arguments()
    
    # Use provided image or create a sample one
    image_path = args.image if args.image else create_sample_image()
    
    # Check if the image file exists
    if not os.path.exists(image_path):
        print(f"エラー: 画像ファイルが見つかりません: {image_path}")
        sys.exit(1)
    
    try:
        # Run image recognition
        print(f"画像を認識中: {image_path}")
        recognize_image(image_path)
        
        print("\nGUIアプリケーションを起動するには:")
        print("  python main.py")
        print("\nコマンドラインインターフェースを使用するには:")
        print(f"  python cli.py {image_path}")
    
    except Exception as e:
        print(f"エラー: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()