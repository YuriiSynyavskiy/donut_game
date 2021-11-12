import pygame


def button_pressed_name(SpriteGroupActive, x, y):
    clicked_sprites = [s for s in SpriteGroupActive if s.rect.collidepoint((x,y))]
    for i in clicked_sprites:
        return str(i)
    return 0


def donut_pressed(DonutGroup, position):
    clicked_sprites = [s for s in DonutGroup if s.rect.collidepoint((position[0],position[1]))]
    for i in clicked_sprites:
        return i
    return 0


def get_indexes_of_donut(tempDonut):
    return (tempDonut.pos_x_in_matrix, tempDonut.pos_y_in_matrix)


def is_in_bounds(indexX, indexY):
    if indexX < 0 or indexX > 6 or indexY < 0 or indexY > 6:
        return False
    return True


def column_of_matrix_by_index(matrix, i):
    return [raw[i] for raw in matrix] 


def check_for_possible_matches(Main_Matrix):
    matches = []
    i = 0; j = 0
    while i < len(Main_Matrix):
        temp_column = column_of_matrix_by_index(Main_Matrix, i)
        while j<len(temp_column)-1:
            temp_j = j
            temp_matches = [temp_column[j]]
            while temp_j+1<=len(temp_column)-1 and temp_column[temp_j].color_index == temp_column[temp_j+1].color_index:
                temp_matches.append(temp_column[temp_j+1])
                temp_j+=1
            j = temp_j
            if len(temp_matches)>=3:
                matches.append(temp_matches)
                j = temp_j
            else:
                j+=1
            temp_matches = []
        i+=1; j=0
        
    i = 0; j = 0
    while i < len(Main_Matrix):  
        while j < len(Main_Matrix)-1:  
            temp_j = j
            temp_matches = [Main_Matrix[i][temp_j]]
            while temp_j+1<=len(Main_Matrix)-1 and Main_Matrix[i][temp_j].color_index == Main_Matrix[i][temp_j+1].color_index:
                temp_matches.append(Main_Matrix[i][temp_j+1])
                temp_j+=1
            if len(temp_matches)>=3:
                matches.append(temp_matches)
                j = temp_j
            else:
                j+=1
            temp_matches = []
        i+=1; j=0
    return matches    