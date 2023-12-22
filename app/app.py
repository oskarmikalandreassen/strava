import matplotlib
matplotlib.use('Agg')  

from flask import Flask, render_template, jsonify, request
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

df = pd.read_csv('app/activities.csv')


selected_options = []


def plot_weekly_activities(df, viewing_options):
    plt.figure(figsize=(12, 5))
    df = df[df['Activity Type'] == 'Run']
    df.loc[:, 'DateTime'] = pd.to_datetime(df['DateTime'])
    df_distance = df.groupby(pd.Grouper(key='DateTime', freq='W-MON'))['Distance'].sum().reset_index()
    df_time = df.groupby(pd.Grouper(key='DateTime', freq='W-MON'))['Moving Time'].sum().reset_index()
    
    if 'kms' in viewing_options:
        plt.plot(df_distance['DateTime'], df_distance['Distance'], marker='o', linestyle='-', color='orange', label='Distance (kms)', markerfacecolor='white', markersize=10)
        plt.fill_between(df_distance['DateTime'], df_distance['Distance'], color='orange', alpha=0.2)
        plt.ylabel('Distance (kms)', fontsize=14)

    if 'time' in viewing_options:
        df_time['Moving Time'] = (df_time['Moving Time'] / 3600).round(1)
        plt.plot(df_time['DateTime'], df_time['Moving Time'], marker='o', linestyle='-', color='blue', label='Moving Time (hours)', markerfacecolor='white', markersize=10)
        plt.fill_between(df_time['DateTime'], df_time['Moving Time'], color='blue', alpha=0.2)
        plt.ylabel('Time (hours)', fontsize=14)

    if 'kms' in viewing_options and 'time' in viewing_options:
        plt.ylabel('Distance (kms) / Moving Time (hours)', fontsize=14)

    plt.title(str(df.iloc[0]['DateTime']).split(' ')[0] + ' - ' + str(df.iloc[-1]['DateTime']).split(' ')[0], fontsize=20)
    plt.xlabel('Date', fontsize=14)
    plt.grid(axis='x')
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    plot_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return plot_base64 

@app.route('/')
def index():
    return render_template('index.html', dataframe=df.to_html())

from datetime import datetime

@app.route('/kms')
def handle_kms_logic():
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')
    selected_options = ['kms']  

    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            filtered_df = df[(pd.to_datetime(df['DateTime']) >= start_date) & (pd.to_datetime(df['DateTime']) <= end_date)]
            plot_data = plot_weekly_activities(filtered_df, selected_options)
            return jsonify({'plot': plot_data})
        except ValueError:
            return jsonify({'error': 'Invalid date format. Please use YYYY-MM-DD format'}), 400
    else:
        return jsonify({'error': 'Please provide valid start and end dates'}), 400

@app.route('/time')
def handle_time_logic():
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')

    selected_options = ['time'] 

    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            filtered_df = df[(pd.to_datetime(df['DateTime']) >= start_date) & (pd.to_datetime(df['DateTime']) <= end_date)]
            plot_data = plot_weekly_activities(filtered_df, selected_options)
            return jsonify({'plot': plot_data})
        except ValueError:
            return jsonify({'error': 'Invalid date format. Please use YYYY-MM-DD format'}), 400
    else:
        return jsonify({'error': 'Please provide valid start and end dates'}), 400



@app.route('/reset_options', methods=['POST'])
def reset_options():
    selected_options.clear()
    return 'Options reset successfully.'

if __name__ == '__main__':
    app.static_folder = 'static'
    app.run(debug=True)
