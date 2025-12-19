import argparse
import os
from PIL import Image
import sys

def resize_images(input_dir, output_dir, max_width=1280, quality=85):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Supported image extensions
    valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff'}

    count = 0
    
    # Iterate through files in input directory
    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        
        # Skip directories
        if not os.path.isfile(file_path):
            continue

        # Check extension
        ext = os.path.splitext(filename)[1].lower()
        if ext not in valid_extensions:
            continue

        output_path = os.path.join(output_dir, filename)

        try:
            with Image.open(file_path) as img:
                width, height = img.size
                
                # Determine save parameters based on format
                save_kwargs = {}
                if ext in {'.jpg', '.jpeg'}:
                    save_kwargs['quality'] = quality
                    save_kwargs['optimize'] = True
                elif ext == '.png':
                    save_kwargs['optimize'] = True
                elif ext == '.webp':
                    save_kwargs['quality'] = quality

                if width > max_width:
                    # Calculate new height maintaining aspect ratio
                    ratio = max_width / width
                    new_height = int(height * ratio)
                    
                    # Resize using high-quality resampling
                    resized_img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                    
                    # Save resized image with optimization
                    resized_img.save(output_path, **save_kwargs)
                    print(f"Resized & Optimized: {filename} ({width}x{height} -> {max_width}x{new_height})")
                else:
                    # Save original image with optimization
                    img.save(output_path, **save_kwargs)
                    print(f"Optimized: {filename} (Width {width} <= {max_width})")
                
                count += 1

        except Exception as e:
            print(f"Error processing {filename}: {e}")

    print(f"\nDone! Processed {count} images.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resize and optimize images in a directory.")
    parser.add_argument("--in", dest="input_dir", required=True, help="Input directory path")
    parser.add_argument("--out", dest="output_dir", required=True, help="Output directory path")
    parser.add_argument("--quality", type=int, default=85, help="Image quality (1-100) for JPG/WebP. Default: 85")
    
    args = parser.parse_args()
    
    # Validate input directory
    if not os.path.exists(args.input_dir):
        print(f"Error: Input directory '{args.input_dir}' does not exist.")
        sys.exit(1)

    resize_images(args.input_dir, args.output_dir, quality=args.quality)
