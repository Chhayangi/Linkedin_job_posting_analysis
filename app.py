import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px


st.title("LinkedIn Job Postings Analysis")
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    # Read the file
    df = pd.read_excel(uploaded_file)
    pd.set_option('display.max_columns',None)
    st.success("File Uploaded Successfully")
    st.subheader("Preview of Data")
    cols = ["job_title","industry","employment_type","location","seniority_level"]
    df = df[cols].head(151)
    df_subset = df.head(150)

    st.dataframe(df)
   
    # Rename column to fix any spaces
    df.rename(columns={"employment _type": "employment_type"}, inplace=True)

    # Drop rows with missing job titles or employment type
    df = df.dropna(subset=['job_title', 'employment_type'])

    # Clean column names first
    df.columns = df.columns.str.strip()
    # Example path: location → employment_type → seniority_level
    df_clean = df_subset.dropna(subset=['location', 'employment_type', 'seniority_level'])


    

    # Sidebar for selecting chart
    option = st.sidebar.radio("Choose a visualization",['Top Job Titles (Bar Graph)','Top Industries (Bar Graph)', 'Top Job Title (Word Cloud)', 
                                                        'Employment Type (Pie Chart)','Job Location (Sunbrust Chart)'])
    
    if option == 'Top Job Titles (Bar Graph)':
        top_jobs = df['job_title'].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(15,15))
        bars = ax.barh(top_jobs.index, top_jobs.values, color='orchid')
        ax.set_xlabel('Count',fontsize = 20)
        ax.set_ylabel('Job Title' ,fontsize = 20)
        ax.set_title('Top 10 Job Titles' , fontsize = 20)
        ax.tick_params(axis='both',labelsize=15)
        ax.invert_yaxis()
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.5, bar.get_y() + bar.get_height()/2,
                    str(int(width)), va='center',fontsize = 20)
        st.pyplot(fig)

    elif option == 'Top Industries (Bar Graph)':
        top_industries = df['industry'].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(15,15))
        top_industries.plot(kind='barh', color='pink', ax=ax)
        ax.set_xlabel('Count',fontsize = 20)
        ax.set_ylabel('Industry' , fontsize = 20)
        ax.set_title('Top 10 Industries' , fontsize = 20)
        ax.tick_params(axis='both',labelsize=15)
        ax.invert_yaxis()
        for i, v in enumerate(top_industries):
            ax.text(v + 0.2, i, str(v), color='black', va='center' , fontsize = 20)
        st.pyplot(fig)
        
    elif option == 'Top Job Title (Word Cloud)':
        text = ' '.join(df['job_title'].dropna().astype(str))
        # wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        fig, ax = plt.subplots(figsize=(20,20))
        # ax.imshow(wordcloud, interpolation='bilinear')
        wordcloud = WordCloud(
        width=800,height=400,background_color='black',
        font_path ='C:/Users/PC-HP/Downloads/Oswald/Oswald-VariableFont_wght.ttf',colormap='rainbow', max_words=200,             
        contour_width=2,contour_color='white',prefer_horizontal=0.9, max_font_size=80,relative_scaling=0.5,    
        collocations=False).generate(text)
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
        
    elif option == 'Employment Type (Pie Chart)':
        emp_counts = df['employment_type'].value_counts()
        fig, ax = plt.subplots(figsize=(15,15))
        ax.set_title('Employment Types',fontsize = 20)
        
        labels = df['employment_type'].value_counts().index
        sizes = df['employment_type'].value_counts().values
        
        wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',startangle=140,textprops={'fontsize': 14}, labeldistance=1.05,wedgeprops={'edgecolor': 'black'},colors=plt.cm.Set3.colors)
        ax.axis('equal')
        st.pyplot(fig)


    elif option == 'Job Location (Sunbrust Chart)':
        df_clean = df.dropna(subset=['location', 'employment_type', 'seniority_level'])
        df_clean = df_clean[df_clean['seniority_level'].str.strip() != '']

        top_locations = df_clean['location'].value_counts().head(8).index
        df_filtered = df_clean[df_clean['location'].isin(top_locations)]

        fig= px.sunburst(df_filtered,path=['location', 'employment_type', 'seniority_level'], 
                         values=None,  
                         title='Sunburst Chart of Job Locations by Employment Type and Seniority Level')
        
        fig.update_layout(width=1000,
                          height=800,
                          margin=dict(t=100, l=50, r=50, b=50),
                        #   font=dict(color='black', size=14)
        )       
        st.plotly_chart(fig)
        
else:
    st.warning("Please upload an Excel file to begin.")

#open new terminal and write streamlit run python.py




