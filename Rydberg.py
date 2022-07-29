import numpy as np
import xlrd
import matplotlib.pyplot as plt
wb=xlrd.open_workbook(r"D:\Research\1\optimized excel files\Ahmed's Elements.xls")
sheet=wb.sheet_by_index(0)

print('\nDo you want to draw energy level diagram or Quantum defect graph or Energy graph?')
print('\nselect 1 for energy level graph, 2 for Quantum defect graph and for Energy graph')
select=input('select 1 or 2 = ')

"======================================"
"This portion is for elements selection"
"======================================"

print('\nfollowing are the elements whose energy Q.D can be calculated by this Program')
elements=[]
for row in range(sheet.nrows):
    elements.append(sheet.cell_value(row,0))

atom=[]
for i in range(0,len(elements)):
    if elements[i]!=elements[i-1]:
        atom.append(elements[i])

print(atom)

print("Data you are looking for,is shown here in our database? , please enter  :")
yn=input("'yes' or 'no' :\n")

suborbitals=['s','p','d','f','g','h','i']
l=[0,1,2,3,4,5,6]
R=109737.3
Enet=[]

if yn=='yes':
    element = input('choose one of the symbol = ')
        
    "======================================"
    "Elements' Data Extraction from Excel file"
    "======================================"
    orbital=[]
    spin=[]
    config=[]
    I=[]
    n1=[]
    E1=[]
    for row in range(sheet.nrows):
        if sheet.cell_value(row,0)==element:
            orbital.append(sheet.cell_value(row,4))
            spin.append(sheet.cell_value(row,3))
            config.append(sheet.cell_value(row,2))
            I=sheet.cell_value(row,6)
            n1.append(sheet.cell_value(row,5))
            E1.append(sheet.cell_value(row,1))
            
    "================================="
    "Arranging data w.r.t Energy levels"
    "================================="
        
    data=[]    
    orbitals=[]
    o=[]
    E=[]
    n=[]
    sp=[]
    
    for k in range(0,len(suborbitals)):
        for i in range(0,len(orbital)):
            if suborbitals[k]==orbital[i]:
                o1=orbital[i]
                o.append(o1)
                E11=E1[i]
                E.append(E11)
                n11=n1[i]
                n.append(n11)
                spin1=spin[i]
                sp.append(spin1)
        for  i in range(0,len(o)):
            if suborbitals[k]==o[i]:
                j=l[k]            
                data1=[j,o[i],E[i],n[i],sp[i]]
                data.append(data1)
    
    
    "==========================="
    "Quantum Defects calculation"
    "==========================="
    for p in range(0,1+data[-1][0]):
        E=[]
        n=[]
        for i in range(0,len(data)):
            if p==data[i][0]:
                n.append(data[i][3])
                E.append(data[i][2])
        x=3
        if len(n)>3:
            x=4
            dn=[]
            for i in range(0,x):
                dn.append(n[i]-(R/(I-E[i]))**0.5)
                
            "========================================="
            "Quantum Defects' coefficients calculatoin"
            "========================================="
            
            do=dn[0]
            
            col=[]
            for i in range(0,x):  
                row=[]
                for j in range(0,x):
                    row.append(1/(n[i]-do)**(2*j))
                col.append(row)
            
            col=np.transpose(col)
            colinv=np.linalg.inv(col)
            
            dn=np.array(dn)
            
            coeff=np.matmul(dn,colinv)
        
            m=np.linspace(int(min(n)),50,51-int(min(n)))
            delta=[]
            E11=[]
            suborbitals1=[]
            for i in range(0,len(m)):                          
                sum=0
                for j in range(0,x):
                    sum=sum+coeff[j]/(m[i]-do)**(2*j)
                delta.append(sum)
                E11.append(I-R/(m[i]-sum)**2)
                Enet.append([p,I-R/(m[i]-sum)**2,m[i],delta[i]])
                suborbitals1.append(suborbitals[j])
                
if yn=='no':  
    "======================================================="
    "This portion is for user input for unavailable elements"
    "======================================================="
            
    print("\nPlease choose atleast 4 quantum no and Energies of desired orbital w.r.t quantum no and Ionization energy : ")
    element=input("\nPlease enter the element name :\n")
    o=input("Please input orbital e.g: s,p,d,f : ")
    p=suborbitals.index(o)
    
    E=[]
    n=[]  
    for i in range(0,4):

        n1=input("\nPlease enter n" '-' +str(i+1)+ ':'+' ')
        E1=input("\nPlease enter E" '-' +str(i+1)+ ':'+' ')
        E.append(int(E1))
        n.append(int(n1))
    I=int(input("\nPlease input Ionizaton Energy :"))
    Z=int(input("\nplease enter the ionization state 'Z' e.g. for singly ionized state for Na Z=2 etc 'Z' = "))
    x=3
    if len(n)>3:
        x=4
        dn=[]
        for i in range(0,x):
            dn.append(n[i]-(R*Z**2/(I-E[i]))**0.5)
            
        "========================================="
        "Quantum Defects' coefficients calculatoin"
        "========================================="
        
        do=dn[0]
        
        col=[]
        for i in range(0,x):  
            row=[]
            for j in range(0,x):
                row.append(1/(n[i]-do)**(2*j))
            col.append(row)
        
        col=np.transpose(col)
        colinv=np.linalg.inv(col)
        
        dn=np.array(dn)
        
        coeff=np.matmul(dn,colinv)
    
        m=np.linspace(int(min(n)),50,51-int(min(n)))
        delta=[]
        E11=[]
        suborbitals1=[]
        for i in range(0,len(m)):                          
            sum=0
            for j in range(0,x):
                sum=sum+coeff[j]/(m[i]-do)**(2*j)
            delta.append(sum)
            E11.append(I-R*Z**2/(m[i]-sum)**2)
            Enet.append([p,I-R*Z**2/(m[i]-sum)**2,m[i],delta[i]])
            suborbitals1.append(suborbitals[j])
                
if select=='1':
    "============================"
    "Plotting Energy levels Graph"
    "============================"        
    
    for j in range(0,1+Enet[-1][0]):
        for i in range(0,len(Enet)):
            if l[j]== Enet[i][0]:
                plt.plot((j+0.15,j+1),(Enet[i][1],Enet[i][1]))            
    plt.xlim(0,2+Enet[-1][0])
    
    for j in range(0,1+Enet[-1][0]):
    #for i in range(0,j+1):
        x_pos=((j+0.15+j+1)/2)
        y_pos = min(Enet)[1]
        plt.text(x_pos,y_pos, suborbitals[j])
        
    plt.xlabel('orbitals')
    plt.ylabel('Energies')
    plt.title("Element's name "+element)

if select=='2':
    if yn=='yes':
        o=[]
        for i in range(len(Enet)):
            for k in range(len(Enet)):
                if i==Enet[k][0]:
                    o.append(suborbitals[i])
                    break
        print('\nThese are the following orbitals')
        print(o)
        O= input("orbital = ")
        temp=suborbitals.index(O)
    
    else:
        temp=p
        O=o
        
    x=[]
    y=[]
    z=[]
    for k in range(0,len(Enet)):
        if Enet[k][0]==temp: 
            x.append(Enet[k][2])
            y.append(Enet[k][1])
            z.append(Enet[k][3])
    plt1=plt.figure(1)
    plt.plot(x,y)
    plt.xlabel('Quantum No')
    plt.ylabel('Energy Calculated')
    plt.title("Element's name "+element +" "+' orbital-'+O)
    
    plt1=plt.figure(2)
    plt.plot(x,z)            
    plt.xlabel('Quantum No')                     
    plt.ylabel('Quantum Defects')
    plt.title("Element's name "+element +" "+' orbital-'+O)
    plt.show()


