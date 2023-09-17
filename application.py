from flask import Flask,render_template,Blueprint,request
import plotly
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
import json
import os


application = Flask(__name__)
application.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
#views = Blueprint('views', __name__)
#application.register_blueprint(views, url_prefix='/')


data_path = os.getcwd()+'/data'
file_path_1 = data_path + '/train.csv'
cltv_path = data_path + '/customer_ltv.csv'
test_path = data_path + '/test.csv'
df_all = pd.read_csv(file_path_1)
metrics = df_all.columns 
df_cltv = pd.read_csv(cltv_path)
#test_data = pd.read_csv(test_path)
df_cltv_f = df_cltv
sel_col = ['monetary_value','predict_purch_10','predict_purch_30','predict_purch_60','predict_purch_90','prob_alive']
df_cltv_f[sel_col] = round(df_cltv_f[sel_col],2)
df_cltv_f['Churn'] = round(df_cltv_f['Churn'] ,3)
df_cltv_f[['CLV','Revenues']] = round(df_cltv_f[['CLV','Revenues']],0)
#df_cltv_f['InvoiceDate'] = pd.to_datetime(df_cltv_f['InvoiceDate'])
df_cltv_f = df_cltv_f[['CustomerID','Segmentation','Country','CLV','frequency','recency','monetary_value','predict_purch_10','predict_purch_30','predict_purch_60','predict_purch_90','InvoiceDate']]

test_data_t = [list(df_cltv_f.iloc[i]) for i in range(len(df_cltv_f))]
#test_data_t =  [list(test_data.iloc[i]) for i in range(len(test_data))]
head_info = [{"title":item} for item in list(df_cltv_f.columns)]
table_data = {'data':test_data_t,'head':head_info}

roi_data = {'budget':'$1000','cpm':'$8.6','impression':'116,279',
'ctr':'2.3%','clicks':'2,674','conversion':'201',
'rev':'$4,835','profit':'$1,934','roi':'$1.93'}

df_sum = df_cltv.groupby(['Cluster'])['Revenues'].sum().reset_index()
df_sum['Orders'] = df_cltv.groupby(['Cluster'])['Orders'].sum().reset_index()['Orders']
df_sum['Order_Size'] = df_sum['Revenues'] /df_sum['Orders'] 


@application.route('/', methods=['GET', 'POST'])
def index():
    #bar = create_plot('Survived',df_all)
    user_info = get_user_meta(df_cltv)
    country_info = get_country(df_cltv)
    print(country_info.head())
    clv_bar = clv_churn_plot(country_info)
    seg_data = seg_plot(df_cltv)
    return render_template('index.html',plot = clv_bar, seg = seg_data, user_info = user_info,roi_data = roi_data,test_data = table_data)

def create_plot(x_metric, df):
    select_feature = df[x_metric].value_counts()
    data = [
        go.Bar(x=select_feature.index, 
            y=select_feature.values)
    ]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def clv_churn_plot(country_info,x_metric = 'CLV'):
    fig = px.bar(country_info, 
               x = x_metric,
               y = 'Country',
               hover_data = ['Users'],
               custom_data = [x_metric,'Users'],
               orientation='h')  

    if x_metric == 'CLV':
        fig.update_traces(hovertemplate = "<br>".join([
                                "Country: %{y}",
                                x_metric + ": $%{x}",
                                "Users: %{customdata[1]}"])
                                 )

        fig.add_trace(go.Scatter(x = country_info['Users'],
                                 y = country_info['Country'],
                                 customdata = country_info[[x_metric,'Users']],
                                 xaxis = 'x2',name = "", hovertemplate = "<br>".join([
                                "Country: %{y}",
                                x_metric+": $%{customdata[0]}",
                                "Users: %{customdata[1]}"])))
    else:
        fig.update_traces(hovertemplate = "<br>".join([
                                "Country: %{y}",
                                x_metric + ": %{x}%",
                                "Users: %{customdata[1]}"])
                                 )

        fig.add_trace(go.Scatter(x = country_info['Users'],
                                 y = country_info['Country'],
                                 customdata = country_info[[x_metric,'Users']],
                                 xaxis = 'x2',name = "", hovertemplate = "<br>".join([
                                "Country: %{y}",
                                x_metric+": %{customdata[0]}%",
                                "Users: %{customdata[1]}"])))



    fig.update_layout(
        xaxis = {"title": "", "visible":False},
        xaxis2 = {"title": "", "visible":False,"overlaying":"x"},
        yaxis = {"title": ""},
        autosize = False,
        showlegend = False,
        width = 350,
        plot_bgcolor = 'rgba(0, 0, 0, 0)',
        margin=dict(l=20, r=20, t=0, b=20))
    # 
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def seg_plot(df_rftv_final):
    df_rftv_final = df_rftv_final[(df_rftv_final.CLV <10000) & (df_rftv_final.prob_alive >0.75)]
    df_rftv_final['Churn'] = round(100*df_rftv_final['Churn'],1)
    df_rftv_final['CLV'] = round(df_rftv_final['CLV'],0)
    fig = px.scatter(df_rftv_final, x="Churn", y="CLV", hover_data = ['recency'],
                     custom_data = ['Segmentation','recency'],color="Segmentation")
    
    fig.update_traces(hovertemplate = "<br>".join([
                                 "Seg: %{customdata[0]}",
                                "Churn: %{x}%",
                                "CLV: $%{y}",
                                "Recency: %{customdata[1]}"])
                                 )
    fig.update_layout(
        xaxis = {"title": "Churn Prob"},
        yaxis = {"title": "CLV"},   
        legend = {'orientation' : 'h','y':1.2},
        plot_bgcolor = 'rgba(0, 0, 0, 0)',
        margin=dict(l=20, r=20, t=0, b=20))

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def get_user_meta(df_rftv_final):
    users = df_rftv_final['CustomerID'].count()
    churn_prob = round(1 - df_rftv_final['prob_alive'].mean(),3)
    avg_cltv = round(df_rftv_final['CLV'].mean(),0)
    order_num = round(df_rftv_final['Orders'].sum()/users,1)
    order_size = round(df_rftv_final['Revenues'].sum()/df_rftv_final['Orders'].sum(),1)
    user_meta = {"users":users,"churn_prob":str(100*churn_prob) + "%", "avg_cltv": "$" + str(avg_cltv), "order_num":order_num, "order_size": "$"+ str(order_size)}
    return user_meta

def get_country(df_rftv_final):
    by_country = df_rftv_final.groupby(['Country'])['CLV'].mean().reset_index()
    by_country_1 = df_rftv_final.groupby(['Country'])['prob_alive'].mean().reset_index()
    by_country_2  = df_rftv_final.groupby(['Country'])['CustomerID'].count().reset_index()
    by_country = by_country.merge(by_country_1, on = 'Country')
    by_country = by_country.merge(by_country_2, on = 'Country')
    by_country['Churn'] = 100*round(1 - by_country['prob_alive'],3)
    by_country = by_country.sort_values(['CLV'], ascending=[True])
    by_country.rename({'CustomerID': 'Users'}, axis=1, inplace=True)
    by_country['CLV'] = round(by_country['CLV'],0)
    return by_country

#@views.route('/scatter', methods=['GET', 'POST'])
#def change_features():
    #feature = request.args['selected']
    #print(feature)
    #graphJSON = create_plot(feature,df_all)
    #return graphJSON

@application.route('/churn', methods=['GET', 'POST'])
def change_chart():
    feature = request.args['selected']
    #graphJSON = create_plot(feature,df_all)
    if feature == 'churn':
        data_type = 'Churn'
    else:
        data_type = 'CLV'
    country_info = get_country(df_cltv)
    clv_bar = clv_churn_plot(country_info,x_metric = data_type)
    return clv_bar

@application.route('/cba', methods=['GET', 'POST'])
def change_table():
    target = request.args['selected']
    if target == 'hs-a':
        order_size = df_sum['Order_Size'][0]
    elif target == 'ms-ia':
        order_size = df_sum['Order_Size'][1]
    else:
        order_size = df_sum['Order_Size'][2]
    budget = float(request.args['budget'].replace('$', ''))
    cpm = float(request.args['cpm'].replace('$', ''))
    imp = round(budget*1000/cpm,0)
    ctr = float(request.args['ctr'].replace('%', ''))/100
    clicks = imp*ctr
    convert = clicks *0.075
    rev =  convert*order_size
    profit = rev *0.4
    roi = profit/budget
    imp = '{:0,.0f}'.format(imp)
    clicks = '{:0,.0f}'.format(clicks)
    convert = '{:0,.0f}'.format(convert)
    rev = '${:0,.0f}'.format(rev)
    profit = '${:0,.0f}'.format(profit)
    roi  = '${:0,.2f}'.format(roi)
    data = {'imp':imp,'clicks':clicks,'convert':convert,'rev':rev,'profit':profit,'roi':roi}
    return data


@application.route('/model', methods=['GET', 'POST'])
def home():
    return render_template('model.html')


if __name__ == '__main__':
    app.run(debug = True)


