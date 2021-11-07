""""Utilidades para este proyecto."""

def renom_estados(name):
  estados = {
    'Michoacán de Ocampo': 'Michoacán', 
    'México': 'Estado de México', 
    'Veracruz Ignacio de la Llave': 'Veracruz',
    'Coahuila de Zaragoza': 'Coahuila'}

  if name in estados:
    return estados[name]
  
  return name



def get_money(text):

  if pd.isna(text):    
    return np.nan
  re_dinero = re.compile(r'monto de ([\d|,|\.]+) pesos')
  res = re_dinero.search(text)
  if res:
    re_num = re.compile(r'[^0-9]')
    return float(re.sub(re_num, '', res.groups()[0][:-3]))
  return np.nan

  
def get_ds_asf():
  ds_asf = pd.read_csv(
    'https://raw.githubusercontent.com/Erick-INCS/Corruption-analysis/main/datasets/asf_2017-2019.csv',
    encoding='latin-1')
  ds_asf['terminado'] = ds_asf['Estado de Trámite'].isin(['Con seguimiento concluido','Conclusión'])
  ds_asf['desaparecido'] = ds_asf['Texto Acción'].apply(get_money)
  ds_asf['Entidad Federativa'] = ds_asf['Entidad Federativa'].map(renom_estados)
  return ds_asf

def describe_chido(df, columnas = []):
  if columnas:
    df = df[columnas]
  descripcion =df.describe()
  descripcion.loc['IQR'] = descripcion.loc['75%']-descripcion.loc['25%']
  df['desaparecido'].sort_values(ascending= True)
  descripcion.loc['media trunca'] = stats.trim_mean(df, .05)
  descripcion.loc['mediana'] = df.median()
  descripcion.loc['rango'] = df.max() - df.min()
  return descripcion


def get_ds_pres_presi():
    df_pres = pd.read_parquet('https://github.com/Erick-INCS/Corruption-analysis/blob/main/datasets/presupuesto_2017-2020.parquet?raw=true')
    df_pres['ENTIDAD_FEDERATIVA'] = df_pres['ENTIDAD_FEDERATIVA'].map(renom_estados)
    peña = 2013
    df_pres = df_pres[df_pres['CICLO_RECURSO'] >= peña]
    df_pres['es_peña'] = df_pres['CICLO_RECURSO'] < 2019
    return df_pres
