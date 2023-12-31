import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Simple Sales Dashboard", page_icon=":bar_chart:", layout="wide")
#st.set_page_config(page_title="Simple Sales Dashboard", 
#page_icon="https://beaconpowerservices.com/wp-content/uploads/2022/06/BPS-logo-green_BPS-logo-green_favicon_sm.png", layout="wide")
#st.set_page_config(page_title="Simple Sales Dashboard", page_icon="BPS-logo-green_BPS-logo-green_favicon_sm.png", layout="wide")

# ---- READ EXCEL ----
@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(
        io="supermarkt_sales.xlsx",
        engine="openpyxl",
        sheet_name="Sales",
        skiprows=3,
        usecols="B:R",
        nrows=1000,
    )
    # Add 'hour' column to dataframe
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()

# ---- SIDEBAR ----


# Apply custom CSS styling
st.sidebar.markdown(
    """
    <style>
    .custom-header {
        color: #fff;
        font-size: 24px;
        font-weight: bold;
    }

    .custom-label {
        color: #fff;  
    }
    </style>
    """,
    unsafe_allow_html=True
)



# Render the header with custom CSS
st.sidebar.markdown('<h2 class="custom-header">Please Filter Here:</h2>', unsafe_allow_html=True)

st.sidebar.markdown('<h4 class="custom-label">Select the city:</h4>', unsafe_allow_html=True) 
city = st.sidebar.multiselect(
    "",
    options=df["City"].unique(),
    default=df["City"].unique()
)

st.sidebar.markdown('<h4 class="custom-label">Select the Customer Type:</h4>', unsafe_allow_html=True) 
customer_type = st.sidebar.multiselect(
    "",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique(),
)

st.sidebar.markdown('<h4 class="custom-label">Select the Gender:</h4>', unsafe_allow_html=True) 
gender = st.sidebar.multiselect(
    "",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

df_selection = df.query(
    "City == @city & Customer_type ==@customer_type & Gender == @gender"
)

# ---- MAINPAGE ----
st.title(":bar_chart: Dashboard")
st.markdown("##")



# TOP KPI's
total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"GHS {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"GHS {average_sale_by_transaction}")

st.markdown("""---""")

# SALES BY PRODUCT LINE [BAR CHART]
sales_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum(numeric_only=True)[["Total"]].sort_values(by="Total")
)
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#103242"] * len(sales_by_product_line),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# SALES BY HOUR [BAR CHART]
sales_by_hour = df_selection.groupby(by=["hour"]).sum(numeric_only=True)[["Total"]]
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by hour</b>",
    color_discrete_sequence=["#103242"] * len(sales_by_hour),
    template="plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

 

 