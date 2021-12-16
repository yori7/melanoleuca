import argparse
import os
import melanoleuca

parser = argparse.ArgumentParser(prog="Melanoleuca")

parser.add_argument("file")
parser.add_argument("-m", "--min", nargs=3, default=[0, 0, 0])
parser.add_argument("-M", "--max", nargs=3, default=[255, 255, 255])
parser.add_argument("-c", "--color", nargs=3, default=None)
parser.add_argument("-a", "--allow", default=0)
parser.add_argument("-o", "--out", default=".")

args = parser.parse_args()

if args.color:
    base_color = [int(i) for i in args.color]
    allow = args.allow / 100
    rgb_min = [rgb * (1 + allow) for rgb in base_color]
    rgb_max = [rgb * (1 - allow) for rgb in base_color]
else:
    rgb_min = [int(i) for i in args.min]
    rgb_max = [int(i) for i in args.max]

fname = os.path.abspath(args.file)
outDir = os.path.abspath(args.out)
basename = os.path.basename(fname)
mark_name = outDir + "/" + basename + "_mark.jpg"
mask_name = outDir + "/" + basename + "_BW.jpg"

mark, mask = melanoleuca.change_img(fname, *rgb_min, *rgb_max)
mark.save(mark_name)
mask.save(mask_name)
