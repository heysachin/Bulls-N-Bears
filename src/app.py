from datetime import datetime
import time


def file_len(fileName):
    with open(fileName) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def printCSV(fname, header="id"):
    import pandas
    df = pandas.read_csv(fname,index_col=header)
    print(df)


option = 0
while option != 15:
    option = int(input("1. Add A Team\n"
                       "2. Display Status of Teams\n"
                       "3. Buy Stock\n"
                       "4. Sell Stock\n"
                       "5. View Stock Book\n"
                       "6. View History\n"
                       "7. View Stock Prices\n"
                       "15. Exit\n\n"
                       "Enter Option : "));

    if option == 1:
        Name = input("Input Name of The Team : ")
        Cash=input("Enter the starting Money of the team : ")
        uid=file_len("team.csv")
        writeText=str(uid)+","+str(Name)+","+str(Cash)+"\n"
        teamFile=open("team.csv", "a")
        teamFile.write(writeText)
        teamFile.close()
        IndividualFile=open("Teams/"+str(uid)+".csv", "w")
        IndividualFile.write("TimeStamp,Activity,Stock,Quantity,Balance\n")
        st = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        IndividualFile.write(str(st)+",Created Account,0,0,"+str(Cash))
        IndividualFile.close()
        StockBook = open("StockBook/" + str(uid) + ".csv", "w")
        StockBook.write("Company ID,Company Name,Stock Amount\n"
                        "1,Elxi,0\n"
                        "2,Tata,0\n"
                        "3,Mango,0")
        StockBook.close()
    elif option == 2:
        printCSV("team.csv")
        print("\n")
    elif option == 3:
        Round = input("Enter the Round : ")
        printCSV("PriceList/batch"+str(Round)+".csv")
        print("\n\n")
        batchFile = open("PriceList/batch"+str(Round)+".csv", "r")
        companyRow = batchFile.readline()
        companyID=int(input("Enter The ID of Company you want to Buy : "))
        for i in range(companyID):
            companyRow = batchFile.readline()
        companyRow = companyRow.split(",")
        priceOfStock=int(companyRow[2])

        quantity=int(input("Enter the Quantity of Stock : "))
        printCSV("team.csv")
        id = input("Enter The ID of the Team: ")
        teamFile = open("Teams/"+id + ".csv", "r")
        p = teamFile.read().splitlines()[-1]
        teamFile.close()
        p = p.split(",")
        balanceAmount = int(p[-1])
        IndividualFile = open("Teams/"+ id + ".csv", "a")
        st = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        balanceAfterReduction = int(balanceAmount-(priceOfStock*quantity)-(priceOfStock*quantity*0.05))
        if balanceAfterReduction > 0:
            StockBookFile = open("StockBook/"+id+".csv", "r")
            StockBook = StockBookFile.read().splitlines()
            StockBookFile.close()
            ind = 0
            for i in StockBook[1:]:
                ind += 1
                if int(i.split(",")[0]) == companyID:
                    companyName=i.split(",")[1]
                    newStockBook = StockBook[:ind]
                    modified = ",".join(list(i.split(",")[:-1] + [str(int(i.split(",")[-1]) + quantity)]))
                    newStockBook.append(modified)
                    newStockBook = newStockBook[:] + StockBook[ind + 1:]
                    StockBookFile = open("StockBook/"+id+".csv", "w")
                    for i in newStockBook:
                        StockBookFile.write(str(str(i) + "\n"))
                    StockBookFile.close()
                    IndividualFile.write("\n"+str(st)+",Bought Stock - "+str(companyName)+","+str(priceOfStock)+","+str(quantity)+","+str(balanceAfterReduction))
            MainTeamFile=open("team.csv", "r")
            MainTeam=MainTeamFile.read().splitlines()
            MainTeamFile.close()
            ind=0
            for i in MainTeam[1:]:
                ind += 1
                if i.split(",")[0] == id:
                    newTeam = MainTeam[:ind]
                    modified = ",".join(list(i.split(",")[:-1] + [str(balanceAfterReduction)]))
                    newTeam.append(modified)
                    newTeam = newTeam[:] + MainTeam[ind + 1:]
                    newTeamFile = open("team.csv", "w")
                    for i in newTeam:
                        newTeamFile.write(str(str(i) + "\n"))
                    newTeamFile.close()

        else:
            print("Insufficient Balance")
        IndividualFile.close()
    elif option == 4:
        Round = input("Enter the Round : ")
        printCSV("PriceList/batch" + str(Round) + ".csv")
        print("\n\n")
        batchFile = open("PriceList/batch" + str(Round) + ".csv", "r")
        companyRow = batchFile.readline()
        companyID = int(input("Enter The ID of Company you want to Sell : "))
        for i in range(companyID):
            companyRow = batchFile.readline()
        companyRow = companyRow.split(",")
        priceOfStock = int(companyRow[2])

        quantity = int(input("Enter the Quantity of Stock : "))
        printCSV("team.csv")
        id = input("Enter The ID of the Team: ")
        StockBookFile = open("StockBook/" + id + ".csv", "r")
        StockBook = StockBookFile.read().splitlines()
        StockBookFile.close()
        ind = 0
        for i in StockBook[1:]:
            ind += 1
            if int(i.split(",")[0]) == companyID:
                if int(i.split(",")[-1]) < quantity:
                    print("Sorry, Sufficient Stock Not Available")
                else:
                    teamFile = open("Teams/" + id + ".csv", "r")
                    p = teamFile.read().splitlines()[-1]
                    teamFile.close()
                    p = p.split(",")
                    balanceAmount = int(p[-1])
                    IndividualFile = open("Teams/" + id + ".csv", "a")
                    StockBookFile = open("StockBook/" + id + ".csv", "r")
                    StockBook = StockBookFile.read().splitlines()
                    StockBookFile.close()
                    ind = 0
                    for i in StockBook[1:]:
                        ind += 1
                        if int(i.split(",")[0]) == companyID:
                            companyName = i.split(",")[1]
                            newStockBook = StockBook[:ind]
                            modified = ",".join(list(i.split(",")[:-1] + [str(int(i.split(",")[-1]) - quantity)]))
                            newStockBook.append(modified)
                            newStockBook = newStockBook[:] + StockBook[ind + 1:]
                            StockBookFile = open("StockBook/" + id + ".csv", "w")
                            for i in newStockBook:
                                StockBookFile.write(str(str(i) + "\n"))
                            StockBookFile.close()
                            st = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
                            balanceAfterReduction = int(
                                balanceAmount + (priceOfStock * quantity) - (priceOfStock * quantity * 0.05))
                            IndividualFile.write(
                                "\n" + str(st) + ",Sold Stock - " + str(companyName) + "," + str(priceOfStock) + "," + str(
                                    quantity) + "," + str(balanceAfterReduction))
                    MainTeamFile = open("team.csv", "r")
                    MainTeam = MainTeamFile.read().splitlines()
                    MainTeamFile.close()
                    ind = 0
                    for i in MainTeam[1:]:
                        ind += 1
                        if i.split(",")[0] == id:
                            newTeam = MainTeam[:ind]
                            modified = ",".join(list(i.split(",")[:-1] + [str(balanceAfterReduction)]))
                            newTeam.append(modified)
                            newTeam = newTeam[:] + MainTeam[ind + 1:]
                            newTeamFile = open("team.csv", "w")
                            for i in newTeam:
                                newTeamFile.write(str(str(i) + "\n"))
                            newTeamFile.close()
                    IndividualFile.close()
    elif option == 5:
        printCSV("team.csv")
        id = input("Enter The ID of the Team: ")
        printCSV(str("StockBook/" + id + ".csv"),"Company ID")
        print("\n")
    elif option == 6:
        printCSV("team.csv")
        id = input("Enter The ID of the Team: ")
        printCSV(str("Teams/" + id + ".csv"),"TimeStamp")
        print("\n")
    elif option == 7:
        id = input("Enter The Round Number: ")
        printCSV(str("PriceList/batch" + id + ".csv"))
        print("\n")




