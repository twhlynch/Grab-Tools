# input( block_id )
# check for block_id.png
# check for block_id_side.png
# check for block_id_top.png
# check for block_id_bottom.png
# check for block_id_back.png
# check for block_id_front.png
# check for block_id_side1.png
# check for block_id_side2.png
# check for block_id_side3.png
# check for block_id_side4.png

# pixel gen each side
# assign to 6 sides of square
# place in JSON with each face rotated
# edges are thinner to avoid texture stitching

# 16 x 16 x 16
# 0, 0, 0 => 16, 16 , 0 # front
# 16, 0, 0 => 16, 16, 16 # right
# 16, 0, 16 => 0, 16, 16 # back
# 0, 0, 16 => 0, 16, 0 # left
# 0, 16, 0 => 16, 16, 16 # top
# 0, 0, 0 => 16, 0, 16 # bottom

# output( block_id.level )