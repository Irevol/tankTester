from tank import test_strategy, score_distribution, distribution_data
import streamlit as st
import matplotlib.pyplot as plt

st.header("German Tank Tester")
st.markdown("""
Use the following variables:
- sd (for standard deviation)
- max
- mean
- median
- ss (for sample size)
""")
            
expression_input = st.text_input("Enter expresion", "(sd+max)*0.8")
plot1 = st.checkbox("Plot predictions")
plot2 = st.checkbox("Plot against different sample sizes")

with st.expander("More settings", expanded=False):
    pop_size_input = st.text_input("Population size", "100")
    sample_size_input = st.text_input("Specific sample size", "")
    st.caption(r"By default, tests across sample sizes that are 5% to 20% of the population")

if st.button("Evaluate"):

    #make sure input is ready to roll
    sample_size = None
    expression = None
    pop_size = None

    if sample_size_input != "":
        try:
            sample_size = int(sample_size_input)
        except ValueError:
            st.error(f"Sample size should be a number (got {sample_size_input})")
            exit()
    try:
        pop_size = int(pop_size_input)
    except ValueError:
        st.error(f"Pop. size should be a number (got {sample_size_input})")
        exit()

    expression_input = expression_input.replace("max", "_max")
    expression_input = expression_input.replace("^", "**")
    exec("expression = lambda mean, median, sd, _max, ss, params: "+expression_input)
    if expression == None:
        st.error("Invalid expression")
        exit()

    #numbers
    data = test_strategy(strategy=expression, fixed_ss=None)
    _mean, _median, _sd = distribution_data(data)
    st.markdown(f"""
|  |  |
| -------- | ------- |
| Mean error | {round(pop_size-_mean,3)} ({round(((pop_size-_mean)/pop_size)*100,3)}%) |
| Median error | {round(pop_size-_median,3)} ({round(((pop_size-_median)/pop_size)*100,3)}%) |
| Standard deviation of predictions | {round(_sd,3)} ({round((_sd/pop_size)*100, 3)}%) |
| Probability of within 5% | {round(score_distribution(data),3)} |
""")

    #plot data
    if plot1:
        fig, ax = plt.subplots()
        ax.hist(data, bins=30)
        plt.xlabel(f"Prediction (pop size = {pop_size})")
        plt.ylabel(f"Frequency (10 000 trials)")
        st.pyplot(fig)

    #test across sample sizes 
    if plot2:
        fig, ax = plt.subplots()
        with st.empty():
            st.write("Generating plot... might take a second")
            y = []
            x = []
            for ss in range(5, 25):
                ss = ss/100
                data = test_strategy(strategy=expression, fixed_ss=round(ss*pop_size), n=pop_size)
                score = score_distribution(data, n=pop_size)
                y.append(score)
                x.append(ss)
            plt.xlabel('Sample size proportion of population')
            plt.ylabel(r'Chance of guessing with 5% of pop size')
            ax.scatter(x, y)
            st.write("")
        st.pyplot(fig)
