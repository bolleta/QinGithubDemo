"""
Command Line Interface for Image Recognition

This module provides a command-line interface for the image recognition functionality.
"""

import argparse
import os
import sys
from image_recognition import recognize_image


def parse_arguments():
    """
    Parse command line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="画像認識ツール - 画像内のオブジェクトを認識します"
    )
    
    parser.add_argument(
        "image_path",
        help="認識する画像ファイルのパス"
    )
    
    parser.add_argument(
        "-n", "--top-n",
        type=int,
        default=5,
        help="表示する予測結果の数 (デフォルト: 5)"
    )
    
    return parser.parse_args()


def main():
    """Main entry point for the CLI application."""
    args = parse_arguments()
    
    # Check if the image file exists
    if not os.path.exists(args.image_path):
        print(f"エラー: 画像ファイルが見つかりません: {args.image_path}")
        sys.exit(1)
    
    try:
        # Run image recognition
        print(f"画像を認識中: {args.image_path}")
        recognize_image(args.image_path, args.top_n)
    except Exception as e:
        print(f"エラー: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()