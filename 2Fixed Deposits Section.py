import streamlit as st
import math
import pandas as pd
import altair as alt


if 'fd_df' not in st.session_state:
    st.session_state.fd_df = pd.DataFrame( [] )
    st.session_state.fdinterest = 0.0
#    st.session_state.repayment = 0.0
compfd_mapping = {
    "Daily": 360,
    "Monthly": 12,
    "Quarterly": 4,
    "Half Yearly": 2,
    "Yearly": 1
}

freqfd_mapping = {
    "Days": 360,
    "Months": 12,
    "Quarters": 4,
    "Half Years": 2,
    "Years": 1
}

headfd_mapping = {
    "Daily": "Days",
    "Monthly": "Months",
    "Quarterly": "Quarters",
    "Half Yearly": "Half Years",
    "Yearly": "Years"
}



def showfdaccount():
    reportarr = []
    intrate = st.session_state.fd_rate / 100
    period = st.session_state.fd_term
    maturity = st.session_state.fd_inst
    initial = st.session_state.fd_prin
    yearlycompoundings = compfd_mapping.get(st.session_state.fd_comp)
    yearlyinstalments = freqfd_mapping.get(st.session_state.fd_freq)
    m = 0.0
    roundby = 2
    total1 = 0.0
    total2 = 0.0
    if yearlyinstalments >= yearlycompoundings:
        m = intrate / yearlyinstalments
        fulcomp = int(period / (yearlyinstalments / yearlycompoundings)) 
        balacomp = period - (fulcomp / yearlycompoundings * yearlyinstalments) 
        head1 = st.session_state.fd_freq
        counter = 1
        count1 = 1
        balance = initial
        totint = 0
        totinst = 0
        product = 0
        interest = 0
        while counter <= period:
            product = product + balance
            if math.fmod(counter,yearlyinstalments/yearlycompoundings) == 0:
                interest = round(product * m,2)
                totint = interest + totint
                product = 0.0
            if counter > (fulcomp / yearlycompoundings * yearlyinstalments):
                product = 0
                while count1 <= balacomp:
                    product = product + balance
                    if counter == period:
                        interest = round(product * m,2)
                        totint = interest + totint
                        product = 0
                    if interest > 0.0:
                        reportarr.append(
                            {
                                head1: counter,
                                'Opening Balance': round(balance, roundby),
                                'Interest': round(interest, roundby),
                                'Closing Balance': round(balance + interest, roundby)
                            }    
                        )        
                        balance = balance + interest
                    count1 = count1 + 1
                    counter = counter + 1
                    interest = 0.0
            if counter <= (fulcomp / yearlycompoundings * yearlyinstalments):
                if interest > 0.0:
                    reportarr.append(
                        {
                            head1: counter,
                            'Opening Balance': round(balance, roundby),
                            'Interest': round(interest, roundby),
                            'Closing Balance': round(balance + interest, roundby)
                        }    
                    )        
                    balance = balance + interest
                counter = counter + 1
                interest = 0.0
    elif yearlyinstalments < yearlycompoundings:
        m = intrate / yearlycompoundings  
        n = (yearlycompoundings/yearlyinstalments)
        head1 = headfd_mapping.get(st.session_state.fd_comp)
        counter = 1
        count1 = 1
        instal1 = 0.0
        balance = initial
        totint = 0.0
        totinst = 0.0
        product = 0.0
        interest = 0.0
        comcount = 1
        while counter <= period * yearlycompoundings/yearlyinstalments:
            product = balance + product
            interest = round(product * m,2)
            totint = totint + interest
            product = 0.0
            if interest > 0.0:
                reportarr.append(
                    {
                        head1: counter,
                        'Opening Balance': round(balance, roundby),
                        'Interest': round(interest, roundby),
                        'Closing Balance': round(balance + interest, roundby)
                    }    
                )        
                balance = balance + interest
            counter = counter + 1
            interest = 0.0
    st.session_state.fd_df = pd.DataFrame( reportarr )
    st.session_state.fdinterest = round(totint, roundby)
    


def fd_prin_calc():
    intrate = st.session_state.fd_rate / 100
    period = st.session_state.fd_term
    maturity = st.session_state.fd_inst
    initial = 0.0
    yearlycompoundings = compfd_mapping.get(st.session_state.fd_comp)
    yearlyinstalments = freqfd_mapping.get(st.session_state.fd_freq)
    m = 0.0
    if maturity == 0.0 or intrate == 0.0 or period == 0.0:
        st.error("You have to enter all the other values.!")
    elif yearlyinstalments >= yearlycompoundings:
        m = intrate / yearlyinstalments
        fulcomp = int(period / (yearlyinstalments / yearlycompoundings))
        balacomp = period - (fulcomp / yearlycompoundings * yearlyinstalments) 
        initial = maturity
        initial = initial / (1+(m * balacomp))
        initial = initial / ((1+(intrate / yearlycompoundings))**fulcomp)
    elif yearlyinstalments < yearlycompoundings:
        m = intrate / yearlycompoundings
        initial = maturity / ((1+m)**(period / yearlyinstalments * yearlycompoundings))
    st.session_state.fd_prin = initial        
    showfdaccount()
    
def fd_term_calc():
    intrate = st.session_state.fd_rate / 100
    period = 0.0
    maturity = st.session_state.fd_inst
    initial = st.session_state.fd_prin
    yearlycompoundings = compfd_mapping.get(st.session_state.fd_comp)
    yearlyinstalments = freqfd_mapping.get(st.session_state.fd_freq)
    m = 0.0
    if initial == 0.0 or intrate == 0.0 or maturity == 0.0:
        st.error("You have to enter all the other values!")
    elif maturity <= initial:
        st.error("Maturity amount MUST be greater than the amount invested.")
    elif yearlyinstalments >= yearlycompoundings:
        m = intrate / yearlycompoundings
        x = (math.log(maturity) - math.log(initial)) / math.log(1 + m)
        period = int(x) / yearlycompoundings * yearlyinstalments
        if x - int(x) > 0.0:
            maturity1 = (initial * (1+(intrate / yearlycompoundings))**int(x))
            n = ((maturity/maturity1) - 1) /(intrate / yearlyinstalments)
            period = period + n
    elif yearlyinstalments < yearlycompoundings:
        m = intrate / yearlycompoundings
        x = (math.log(maturity) - math.log(initial)) / math.log(1 + m)
        period = x / yearlycompoundings * yearlyinstalments
    st.session_state.fd_term = round( period )
    showfdaccount()
    

def fd_inst_calc():
    intrate = st.session_state.fd_rate / 100
    period = st.session_state.fd_term
    initial = st.session_state.fd_prin
    maturity = 0.0
    yearlycompoundings = compfd_mapping.get(st.session_state.fd_comp)
    yearlyinstalments = freqfd_mapping.get(st.session_state.fd_freq)
    m = 0.0
    if initial == 0.0 or intrate == 0.0 or period == 0.0:
        st.error("You have to enter all the other values!")
    elif yearlyinstalments >= yearlycompoundings:
        m = intrate / yearlyinstalments
        fulcomp = int(period / (yearlyinstalments / yearlycompoundings))
        balacomp = period - (fulcomp / yearlycompoundings * yearlyinstalments) 
        maturity = (initial * (1+(intrate / yearlycompoundings))**fulcomp) * (1+(m * balacomp))
    elif yearlyinstalments < yearlycompoundings:
        m = intrate / yearlycompoundings
        maturity = initial * (1+m)**(period / yearlyinstalments * yearlycompoundings)
    st.session_state.fd_inst = maturity
    showfdaccount()
    

def fd_rate_calc():
    intrate = 0.0
    period = st.session_state.fd_term
    initial = st.session_state.fd_prin
    maturity = st.session_state.fd_inst
    yearlycompoundings = compfd_mapping.get(st.session_state.fd_comp)
    yearlyinstalments = freqfd_mapping.get(st.session_state.fd_freq)
    m = 0.0
    if maturity == 0.0 or initial == 0.0 or period == 0.0:
        st.error("You have to enter all the other values!")
    elif maturity <= initial:
        st.error("Maturity amount MUST be greater than the amount invested.")
    elif yearlyinstalments >= yearlycompoundings:
        fulcomp = int(period / (yearlyinstalments / yearlycompoundings)) 
        balacomp = period - (fulcomp / yearlycompoundings * yearlyinstalments) 
        if fulcomp > 0:
            m = ((maturity / initial) ** (1 / fulcomp)) - 1
            intrate = m * yearlycompoundings
            if balacomp > 0:
                crossed = False
                while not crossed:
                    m = intrate / yearlyinstalments
                    if (initial * (1+(intrate / yearlycompoundings))**fulcomp) * (1+(m * balacomp)) <= maturity:
                        crossed = True
                    else:
                        intrate = intrate - 0.000001
        else:
            if balacomp > 0:
                intrate = 0.000001
                crossed = False
                while not crossed:
                    m = intrate / yearlyinstalments
                    if (initial * (1+(m * balacomp))) >= maturity:
                        crossed = True
                    else:
                        intrate = intrate + 0.000001
        intrate = intrate * 100
    elif yearlyinstalments < yearlycompoundings:
        x = (period / yearlyinstalments * yearlycompoundings)
        m = ((maturity/initial) ** (1/x)) - 1
        intrate = m * yearlycompoundings * 100
    st.session_state.fd_rate = intrate
    showfdaccount()

    


st.write("# :blue[Fixed Deposits Section]")
[col1, col2] = st.columns([0.3, 0.7])
with col1:
    st.button("Interest Compounding", disabled=True, use_container_width=True)
    st.button("Deposit Amount", on_click=fd_prin_calc, use_container_width=True)
    st.button("Interest Rate (% p.a.)", on_click=fd_rate_calc, use_container_width=True)
    st.button("Term", on_click=fd_term_calc, use_container_width=True)
    st.button("Maturity Value", on_click=fd_inst_calc, use_container_width=True)
    st.button("Instalment Frequency", disabled=True, use_container_width=True)
with col2:
    st.selectbox("Compounding",("Daily", "Monthly", "Quarterly","Half Yearly","Yearly"), label_visibility="collapsed", key="fd_comp")
    st.number_input("Deposit", min_value=0.0, label_visibility="collapsed", key="fd_prin")
    st.number_input("Interest Rate", min_value=0.0, label_visibility="collapsed", key="fd_rate")
    st.number_input("Term", min_value=0.0,  label_visibility="collapsed", key="fd_term")
    st.number_input("Maturity", min_value=0.0, label_visibility="collapsed", key="fd_inst")
    st.selectbox("Frequency",("Days", "Months", "Quarters","Half Years","Years"), label_visibility="collapsed", key="fd_freq")
df = st.session_state.fd_df
if df.shape[0] > 0:
    st.write( df )
    st.write( "Total Interest : " + str( st.session_state.fdinterest) )
    chartdata = df
    chart = alt.Chart(chartdata).mark_area().encode(
        x=chartdata.columns[0]+':O',
        y='Closing Balance:Q',
        tooltip=[chartdata.columns[0], "Closing Balance"]
    )
    st.write(chart)
    st.info("Done!")
    st.session_state.fd_df = pd.DataFrame( [] )
    st.session_state.fdinterest = 0.0
