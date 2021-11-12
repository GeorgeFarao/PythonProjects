from tkinter import *

root = Tk()
root.geometry("350x350")
root.title("Covid-19 Data for each Country")


def showdata():
    from matplotlib import pyplot as plt
    import matplotlib.patches as mpatches
    from covid import Covid

    covid = Covid()
    cases = []
    confirmed = []
    active = []
    deaths = []
    recovered = []

    try:
        global data
        root.update()
        countries = data.get()

        country_names = countries.strip()
        country_names = country_names.replace(" ", ",")
        country_names = country_names.split(",")

        for x in country_names:
            cases.append(covid.get_status_by_country_name(x))
            root.update()
        for y in cases:
            if y["confirmed"] is None:
                confirmed.append(0)
            else:
                confirmed.append(y["confirmed"])
            if y["active"] is None:
                active.append(0)
            else:
                active.append(y["active"])
            if y["deaths"] is None:
                deaths.append(0)
            else:
                deaths.append(y["deaths"])
            if y["recovered"] is None:
                recovered.append(0)
            else:
                recovered.append(y["recovered"])
        print(confirmed,active,recovered,deaths)
        confirmed_patch = mpatches.Patch(color='blue', label='confirmed')
        recovered_patch = mpatches.Patch(color='green', label='recovered')
        active_patch = mpatches.Patch(color='red', label='active')
        deaths_patch = mpatches.Patch(color='black', label='deaths')

        plt.legend(handles=[confirmed_patch, recovered_patch, active_patch, deaths_patch])

        for x in range(len(country_names)):
            n = recovered[x]>active[x]
            plt.bar(country_names[x], confirmed[x], color='blue')
            if recovered[x] > active[x]:
                plt.bar(country_names[x], recovered[x], color='green')
                plt.bar(country_names[x], active[x], color='red')
            else:
                plt.bar(country_names[x], active[x], color='red')
                plt.bar(country_names[x], recovered[x], color='green')
            plt.bar(country_names[x], deaths[x], color='black')

        plt.title('Current Covid Cases')
        plt.xlabel('Country Name')
        plt.ylabel('Cases(in millions)')
        plt.show()
    except Exception as e:
        data.set("Please enter correct details ")


Label(root, text="Enter all country names\n for whom you want to get\nCovid-19 data", font="Consolas 15 bold").pack()
data = StringVar()
data.set("Separate country names using comma or space(not both")
entry = Entry(root, textvariable=data, width=50).pack()
Button(root, text="Get Data", command=showdata).pack()
root.mainloop()
