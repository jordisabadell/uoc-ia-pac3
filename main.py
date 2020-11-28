import json


def executar_funcio(data, nom, valor):

    for v in data['variables']:
        if(v["nom"]==nom):
            
            print("\n" + nom + " = " + str(valor))
            
            resultats = {}        

            #recórrer tots els rangs de la funció de pertinença
            for f in v["funcio_pertinenca"]:
                x = float(valor)

                print(f["nom"].replace("(x)", "(" + str(x)  + ")")) #nomenclatura: U_{nom variable}(x)
                for r in f["rangs"]:
                    
                    #EXECUTAR LA REGLA
                    
                    min = r["rang"].split(",")[0]
                    max = r["rang"].split(",")[1]

                    op_min = min[0].replace("[", "<=").replace("(", "<")
                    num_min = float(min[1:])
                    op_max = max[-1:].replace("]", "<=").replace(")", "<")
                    num_max = float(max[:-1])
                    
                    compleix = False
                    if(op_min=="<=" and num_min<=x):
                        if(op_max=="<=" and x<=num_max):
                            compleix = True
                        elif(op_max=="<" and x<num_max):
                            compleix = True
                    elif(op_min=="<" and num_min<x):
                        if(op_max=="<=" and x<=num_max):
                            compleix = True
                        elif(op_max=="<" and x<num_max):
                            compleix = True
                    
                    print("\tsi " + str(num_min) + " " +  op_min + " " + str(x) 
                        + " " + op_max + " " + str(num_max) + " ? " 
                        + str(compleix))

                    #COMPROVAR SI S'ACTIVA LA REGLA?
                    if compleix:
                        resultat = round(eval(r["valor"].replace(",", ".").replace("x", "*"+str(x))), 4)
                        activa = False
                        if(resultat>0):
                            activa = True
                            nom = f["nom"].replace("U_", "").replace("(x)", "") #nomenclatura: U_{nom variable}(x)
                            resultats[nom] = resultat

                        print("\t=> activa la regla? " + r["valor"] + "... = " + str(resultat) + " ? > 0 " + str(activa))
            return resultats;

def regles_actives(data, nom_varA, resultats_varA, nom_varB, resultats_varB):
    
    for v in data['variables']:
        if(v["nom"]=="regles"):

            resultats = {}
            
            for regla in v["regla"]:
                print("\nAvaluant regla '" + regla + "'")

                #per cada resultat de la variable A, recorrem els de la B
                for resultat_varA in resultats_varA:
                    for resultat_varB in resultats_varB:

                        condicio1 = nom_varA + " es " + resultat_varA
                        condicio2 = nom_varB + " es " + resultat_varB
                        condicio = "si " + condicio1 + " i " + condicio2

                        compleix = False
                        valor = ''
                        if int(regla.find(condicio))>=0:
                            compleix = True
                            valorA = str(resultats_varA[resultat_varA])
                            valorB = str(resultats_varB[resultat_varB])
                            valor = str(valorA) + ", " + str(valorB)
                            valor_min = min(valorA, valorB)

                            resultats[regla] = valor_min
                        print("\t" + condicio + " ? " + str(compleix) 
                                + " " + valor)
                            
            
            return resultats            

def calcular_graus_activacio(regles):
    valors = {}
    for regla in regles:
        resultat = regla.split('llavors')[1]
        resultat = resultat.split('es')[1][1:]
        
        #t-conorma max()
        if not resultat in valors:
            valors[resultat] = regles[regla]
        else:
            if valors[resultat]<regles[regla]: #max
                valors[resultat] = regles[regla]
    return valors

# ------ main -------

nivell_bruticia = 70
nivell_greix = 50

with open('data.json') as json_file:
    data = json.load(json_file)
    
    resultats_varA = executar_funcio(data, 'nivell_greix', nivell_greix)
    print(resultats_varA)

    resultats_varB = executar_funcio(data, 'nivell_bruticia', nivell_bruticia)
    print(resultats_varB)  

    resultats_regles = regles_actives(data, 'nivell_greix', resultats_varA, 
        'nivell_bruticia', resultats_varB)
    print("\nRegles a aplicar:")
    for resultat_regla in resultats_regles:
        print("\t" + resultat_regla + " " + str(resultats_regles[resultat_regla]))


    graus = calcular_graus_activacio(resultats_regles)
    print("Graus d'activació:")
    for grau in graus:
        print("\t" + grau + " = " + graus[grau])