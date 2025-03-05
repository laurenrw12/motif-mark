import cairo
import math

width, height = 2000.6, 200
surface = cairo.PDFSurface("example.pdf", width, height)
context = cairo.Context(surface)

#draw line
context.set_line_width(2)
context.move_to(50,100)        #(x,y)
context.line_to(1950,100)      #(ending x, ending y)
context.stroke()

#draw first exon
context.rectangle(150,50,250,100)        #(x0,y0,x1,y1) (moves left to right, moves up and down, width of box, height of box)
context.fill()

#draw second exon
context.rectangle(850,50,250,100)        
context.fill()

#draw third exon
context.rectangle(1450,50,250,100)        
context.fill()

#write out drawing
surface.finish()



WIDTH, HEIGHT = 256, 256

surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context (surface)

ctx.scale (WIDTH, HEIGHT) # Normalizing the canvas

pat = cairo.LinearGradient (0.0, 0.0, 0.0, 1.0)
pat.add_color_stop_rgba (1, 0.7, 0, 0, 0.5) # First stop, 50% opacity
pat.add_color_stop_rgba (0, 0.9, 0.7, 0.2, 1) # Last stop, 100% opacity

ctx.rectangle (0, 0, 1, 1) # Rectangle(x0, y0, x1, y1)
ctx.set_source (pat)
ctx.fill ()

ctx.translate (0.1, 0.1) # Changing the current transformation matrix

ctx.move_to (0, 0)
# Arc(cx, cy, radius, start_angle, stop_angle)
ctx.arc (0.2, 0.1, 0.1, -math.pi/2, 0)
ctx.line_to (0.5, 0.1) # Line to (x,y)
# Curve(x1, y1, x2, y2, x3, y3)
ctx.curve_to (0.5, 0.2, 0.5, 0.4, 0.2, 0.8)
ctx.close_path ()

ctx.set_source_rgb (0.3, 0.2, 0.5) # Solid color
ctx.set_line_width (0.02)
ctx.stroke ()

surface.write_to_png ("example2.png") # Output to PNG



