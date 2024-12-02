from django.shortcuts import render

import csv
from django.shortcuts import render
from .models import EnergyData
from .forms import CSVUploadForm
from django.contrib import messages
from django.core.paginator import Paginator
import plotly.express as px # type: ignore
import pandas as pd  # type: ignore


def import_csv(request):
    csv_data = [] 

    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        data = csv_file.read().decode('utf-8').splitlines()

        # Nettoyer le BOM (Byte Order Mark) s'il y'en a 
        if data[0].startswith('\ufeff'):
            data[0] = data[0][1:]  # Retirer le BOM

        reader = csv.DictReader(data, delimiter=',')

        for row in reader:
            try:
                date = row.get('Date', '').strip()
                region = row.get('Region', '').strip()
                consumption_str = row.get('Valeur (TWh)', '0').strip()
                consumption_str = consumption_str.replace(',', '.')  
                consumption_twh = float(consumption_str) 


                if date and region:  
                    energy_data = EnergyData.objects.create(
                        date=date,
                        region=region,
                        consumption_twh=consumption_twh
                    )

                    # Ajouter les données importées dans la liste csv_data
                    csv_data.append({
                        'Date': energy_data.date,
                        'Region': energy_data.region,
                        'Consommation (TWh)': energy_data.consumption_twh
                    })

                    print(f"Donnée importée: Date={energy_data.date}, Région={energy_data.region}, Consommation={energy_data.consumption_twh} TWh")

            except KeyError as e:
                messages.error(request, f"Erreur dans le fichier CSV, clé manquante: {e}")
                return render(request, 'myAppData/import_csv.html', {'form': CSVUploadForm()})
            except ValueError as e:
                messages.error(request, f"Erreur dans le fichier CSV, problème de conversion de valeur: {e}")
                return render(request, 'myAppData/import_csv.html', {'form': CSVUploadForm()})

        messages.success(request, 'Le fichier CSV a été importé avec succès.')

    # Pagination des données importées
    energy_data_list = EnergyData.objects.all().order_by('-date')
    paginator = Paginator(energy_data_list, 10)  # Afficher 10 par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'myAppData/import_csv.html', 
        {'form': CSVUploadForm(),
         'page_obj': page_obj,
         'csv_data': csv_data, 
        })


def consumption_by_region(request):
    energy_data = EnergyData.objects.all().values('region', 'consumption_twh')
    df = pd.DataFrame(energy_data)

    # Créer un graphique interactif avec Plotly
    fig = px.bar(df, x='region', y='consumption_twh', title="Consommation par région")

    # Convertir le graphique en HTML pour l'affichage
    graph_html = fig.to_html(full_html=False)

    return render(request, 'myAppData/consumption_by_region.html', {'graph_html': graph_html})



def consumption_by_year(request):
    # Récupérer les données de consommation
    energy_data = EnergyData.objects.all().values('consumption_twh', 'date')

    # Créer un DataFrame à partir des données
    df = pd.DataFrame(energy_data)

    df['year'] = pd.to_datetime(df['date']).dt.year

    df_yearly = df.groupby('year').agg({'consumption_twh': 'sum'}).reset_index()

    # Créer un graphique interactif de la consommation par année
    fig_year = px.line(df_yearly, x='year', y='consumption_twh', title="Consommation en France par année")

    # Convertir le graphique en HTML pour l'affichage
    graph_html_year = fig_year.to_html(full_html=False)

    return render(request, 'myAppData/consumption_by_year.html', {
        'graph_html_year': graph_html_year
    })




