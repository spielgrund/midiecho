import pygame
import pygame_widgets
import pygame.freetype
import mido
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.dropdown import Dropdown
from pygame_widgets.button import Button

pygame.init()

# Set up Pygame window
width, height = 600, 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame MIDI App")
my_font = pygame.freetype.Font("freepix.ttf", 12)

input_port = "dont crash"
output_port = "dont crash"


#Select the Midi Device here
def update_ports(choice1=0,choice2=1):
    # List available MIDI input ports
    global input_port
    global output_port
    global input_ports
    global output_ports
    
    input_ports = mido.get_input_names()
    output_ports = mido.get_output_names()

    print("Available MIDI input ports:", input_ports)
    print("Available MIDI output ports:", output_ports)

    # Open the first available MIDI input port
    if input_ports and output_ports:
        input_port_name = input_ports[choice1]

        
        input_port = mido.open_input(input_port_name)
        print(f"Using MIDI input port: {input_port_name}")

        output_port_name = output_ports[choice2]

        
        output_port = mido.open_output(output_port_name)
        print(f"Using MIDI output port: {output_port_name}")
        
    else:
        print("No available MIDI input ports.")
        #pygame.quit()
        #quit()

update_ports()
def ports():
    if input_port != "dont crash":
        if not input_port.closed:
            input_port.close()
        if not output_port.closed:
            output_port.close()
    
    i,j = 0,0

    if dropdown_in.getSelected() != None:
        i = dropdown_in.getSelected()
    if dropdown_out.getSelected() != None:
        j = dropdown_out.getSelected()

    
    update_ports(i,j)
    print(input_port)
    print(output_port)
#ports()


text_surface1, rect = my_font.render('Midi 2', (0, 0, 0))
text_surface2, rect = my_font.render('Midi 3', (0, 0, 0))
text_surface3, rect = my_font.render('Midi 4', (0, 0, 0))
text_surface11, rect = my_font.render(' Vel 1', (0, 0, 0))
text_surface22, rect = my_font.render(' Vel 2', (0, 0, 0))
text_surface33, rect = my_font.render(' Vel 3', (0, 0, 0))
text_surface111, rect = my_font.render('Note 1', (0, 0, 0))
text_surface222, rect = my_font.render('Note 2', (0, 0, 0))
text_surface333, rect = my_font.render('Note 3', (0, 0, 0))

# Checkbox properties
checkbox1_rect = pygame.Rect(50, 50, 20, 20)
checkbox1_checked = False
checkbox2_rect = pygame.Rect(150, 50, 20, 20)
checkbox2_checked = False
checkbox3_rect = pygame.Rect(250, 50, 20, 20)
checkbox3_checked = False

slider1 = Slider(screen, 40, 105, 50, 10, min=2, max=100, step=1, initial=100)
output1 = TextBox(screen, 50, 130, 30 , 20, fontSize=12)
output1.disable()  # Act as label instead of textbox

slider11 = Slider(screen, 40, 185, 50, 10, min=0, max=48, step=1, initial=24)
output11 = TextBox(screen, 50, 210, 30 , 20, fontSize=12)
output11.disable()  # Act as label instead of textbox

slider2 = Slider(screen, 140, 105, 50, 10, min=2, max=100, step=1, initial=100)
output2 = TextBox(screen, 150, 130, 30 , 20, fontSize=12)
output2.disable()  # Act as label instead of textbox

slider22 = Slider(screen, 140, 185, 50, 10, min=0, max=48, step=1, initial=24)
output22 = TextBox(screen, 150, 210, 30 , 20, fontSize=12)
output22.disable()  # Act as label instead of textbox

slider3 = Slider(screen, 240, 105, 50, 10, min=2, max=100, step=1, initial=100)
output3 = TextBox(screen, 250, 130, 30 , 20, fontSize=12)
output3.disable()  # Act as label instead of textbox

slider33 = Slider(screen, 240, 185, 50, 10, min=0, max=48, step=1, initial=24)
output33 = TextBox(screen, 250, 210, 30 , 20, fontSize=12)
output33.disable()  # Act as label instead of textbox

############################# Dropdown
def set_midi_in():
    print(dropdown_in.getSelected())

l_in = [i for i in range(len(input_ports))]
dropdown_in = Dropdown(
    screen, 350, 40, 100, 30, name='  Midi In',
    choices=input_ports,
    borderRadius=3, colour=pygame.Color('grey'), values=l_in, direction='down', textHAlign='left'
)
l_out = [i for i in range(len(output_ports))]
dropdown_out = Dropdown(
    screen, 350, 120, 150, 30, name='  Midi Out',
    choices=output_ports,
    borderRadius=3, colour=pygame.Color('grey'), values=l_out, direction='down', textHAlign='left'
)

button = Button(
    screen, 350, 200, 150, 50, text='Update Ports', fontSize=30,
    margin=20, inactiveColour=(255, 0, 0), pressedColour=(0, 255, 0),
    radius=5, onClick=ports, font=pygame.font.SysFont('calibri', 10),
    textVAlign='bottom'
)




running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if checkbox1_rect.collidepoint(event.pos):
                checkbox1_checked = not checkbox1_checked
            if checkbox2_rect.collidepoint(event.pos):
                checkbox2_checked = not checkbox2_checked
            if checkbox3_rect.collidepoint(event.pos):
                checkbox3_checked = not checkbox3_checked

    if input_port != "dont crash":
        for msg in input_port.iter_pending():
            # Handle MIDI messages
            s = str(msg)
            if s[0] == "n":
                split = s.split()
                note_on,c, n, v = split[0],split[1],split[2],split[3]
                #msg = f"{note_on},{channel},{note},{velocity}"
                n = int(n.replace("note=",""))
                #v = int(v.replace("velocity=",""))
                msg = mido.Message(note_on,note=n)
                
                if checkbox1_checked:
                    n1 = n + slider11.getValue()-24
                    msg1 = msg.copy(channel=1,note=n1,velocity=slider1.getValue())
                    print(msg1)
                    output_port.send(msg1)

                if checkbox2_checked:
                    n2 = n + slider22.getValue()-24
                    msg2 = msg.copy(channel=2,note=n2,velocity=slider2.getValue())
                    print(msg2)
                    output_port.send(msg2)

                if checkbox3_checked:
                    n3 = n + slider33.getValue()-24
                    msg3 = msg.copy(channel=3,note=n3,velocity=slider3.getValue())
                    print(msg3)
                    output_port.send(msg3)
                    

    screen.fill((255, 255, 255))

    # Draw checkbox
    pygame.draw.rect(screen, BLACK, checkbox1_rect, 2)
    pygame.draw.rect(screen, BLACK, checkbox2_rect, 2)
    pygame.draw.rect(screen, BLACK, checkbox3_rect, 2)
    if checkbox1_checked:
        pygame.draw.rect(screen, BLACK, checkbox1_rect, 0)
    if checkbox2_checked:
        pygame.draw.rect(screen, BLACK, checkbox2_rect, 0)
    if checkbox3_checked:
        pygame.draw.rect(screen, BLACK, checkbox3_rect, 0)
    
    
    output1.setText(slider1.getValue())
    output11.setText(slider11.getValue()-24)
    output2.setText(slider2.getValue())
    output22.setText(slider22.getValue()-24)
    output3.setText(slider3.getValue())
    output33.setText(slider33.getValue()-24)

    screen.blit(text_surface1, (40,30))
    screen.blit(text_surface2, (140,30))
    screen.blit(text_surface3, (240,30))
    screen.blit(text_surface11, (40,85))
    screen.blit(text_surface22, (140,85))
    screen.blit(text_surface33, (240,85))
    screen.blit(text_surface111, (40,165))
    screen.blit(text_surface222, (140,165))
    screen.blit(text_surface333, (240,165))

    pygame_widgets.update(event)
    pygame.display.flip()

pygame.quit()
input_port.close()
