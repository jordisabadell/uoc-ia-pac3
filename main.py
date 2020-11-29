import json

DEBUG = True

def executar_funcio(data, nom, valor):

    for v in data['variables']:
        if(v["nom"]==nom):
            
            if DEBUG: print("\n" + nom + " = " + str(valor))
            
            resultats = {}

            #recórrer tots els rangs de la funció de pertinença
            for f in v["funcio_pertinenca"]:
                x = float(valor)

                if DEBUG: print(f["nom"].replace("(x)", "(" + str(x)  + ")")) #nomenclatura: U_{nom variable}(x)
                for r in f["rangs"]:
                    
                    #EXECUTAR LA REGLA
                    #if DEBUG: print(r["rang"])
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
                    
                    if DEBUG: print("\tsi " + str(num_min) + " " +  op_min + " " + str(x) 
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
                        
                        if DEBUG: print("\t=> revisant si activa la regla? Avaluant y=" + r["valor"] + "=" + str(resultat) + " > 0? " + str(activa))
            return resultats;

def regles_actives(data, nom_varA, resultats_varA, nom_varB, resultats_varB):
    
    for v in data['variables']:
        if(v["nom"]=="regles"):

            resultats = {}
            
            i=1
            for regla in v["regla"]:
                if DEBUG: print("\nAvaluant regla " + str(i) + " '" + regla + "'")

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
                            valor = "min(" + str(valorA) + ", " + str(valorB) + ")"
                            valor_min = min(valorA, valorB)

                            regla = str(i) + ": " + regla

                            resultats[regla] = valor_min
                        if DEBUG: print("\t" + condicio + " ? " + str(compleix) 
                                + " " + valor)
                i=i+1    
            
            return resultats            

def calcular_graus_activacio(regles):
    
    if DEBUG: print("\nCalculant graus d'activació: ")
    
    valors = {}
    for regla in regles:
        resultat = regla.split('llavors')[1]
        resultat = resultat.split('es')[1][1:]
        
        #t-conorma max()
        if not resultat in valors:
            if DEBUG: print("\tResultat " + str(resultat) + " repetit? False")
            valors[resultat] = regles[regla]
        else:
            if DEBUG: print("\tResultat " + str(resultat) + " repetit? True max(" + str(valors[resultat]) + ", " + str(regles[regla]) + ")")
            if valors[resultat]<regles[regla]: #max
                valors[resultat] = regles[regla]
    return valors

# ------ main -------

with open('data-outplanta.json') as json_file:
    data = json.load(json_file)

    varA_nom = data["variableA"]["nom"]
    varA_valor_entrada = data["variableA"]["valor_entrada"]

    varB_nom = data["variableB"]["nom"]
    varB_valor_entrada = data["variableB"]["valor_entrada"]
    
    print("\n# Valors que activen les variables:")

    resultats_varA = executar_funcio(data, varA_nom, varA_valor_entrada)
    print("\n# " + varA_nom + "=" + varA_valor_entrada + " activa " + str(resultats_varA))

    resultats_varB = executar_funcio(data, varB_nom, varB_valor_entrada)
    print("\n# " + varB_nom + "=" + varB_valor_entrada + " activa " + str(resultats_varB))

    resultats_regles = regles_actives(data, varA_nom, resultats_varA, 
        varB_nom, resultats_varB)
    print("\n# Regles que s'activen aplicant 't-norma min':")
    for resultat_regla in resultats_regles:
        print("\t" + resultat_regla + " {" + str(resultats_regles[resultat_regla]) + "}")

    graus = calcular_graus_activacio(resultats_regles)
    print("\n# Termes que s'activen i nivell resultant aplicant t-conorma max:")
    for grau in graus:
        print("\t" + grau + " = " + graus[grau])