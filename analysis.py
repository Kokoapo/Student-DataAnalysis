import pandas as pd
import streamlit as st
import plotly.express as px

def get_mean(dataframe: pd.DataFrame, column_name):
    return dataframe[column_name].mean()

def average_scores(dataframe: pd.DataFrame):
    st.header("Average Scores")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("Focus")
        avg_focus_score = get_mean(dataframe, "focus_score")
        st.write(f"**{avg_focus_score:.2f} points**")
    with c2:
        st.subheader("Productivity")
        avg_productivity_score = get_mean(dataframe, "productivity_score")
        st.write(f"**{avg_productivity_score:.2f} points**")
    with c3:
        st.subheader("Final Grade")
        avg_final_grade = get_mean(dataframe, "final_grade")
        st.write(f"**{avg_final_grade:.2f} points**")

def scores_correlation(dataframe: pd.DataFrame):
    st.header("Correlation Scores")
    
    data = dataframe[["focus_score", "productivity_score", "final_grade", "stress_level"]]
    fig = px.scatter(data,
                    x='focus_score',
                    y='final_grade',
                    size='productivity_score',
                    color='productivity_score',)
    fig.update_layout(title="Correlation between Scores",
                    xaxis_title="Focus Score",
                    yaxis_title="Final Grade",
                    coloraxis_colorbar=dict(title="Productivity Score"))
    st.plotly_chart(fig, use_container_width=True)

def correlations_productivity(dataframe: pd.DataFrame):
    st.header("Correlations with Productivity Score")

    data = dataframe[["productivity_score", "phone_usage_hours", "study_hours_per_day", ]]
    c1, c2 = st.columns(2)
    with c1:
        fig = px.scatter(data,
                        x='phone_usage_hours',
                        y='productivity_score')
        fig.update_layout(title="Phone Usage vs Productivity Score",
                        xaxis_title="Phone Usage (hours)",
                        yaxis_title="Productivity Score")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.scatter(data,
                        x='study_hours_per_day',
                        y='productivity_score',)
        fig.update_layout(title="Study Hours vs Productivity Score",
                        xaxis_title="Study Hours per Day",
                        yaxis_title="Productivity Score")
        st.plotly_chart(fig, use_container_width=True)

def pie_daily_hours(dataframe: pd.DataFrame):
    st.header("Average Hours Spent per Day")

    avg_study_hours = get_mean(dataframe, "study_hours_per_day")
    avg_sleep_hours = get_mean(dataframe, "sleep_hours")
    avg_phone_usage_hours = get_mean(dataframe, "phone_usage_hours")
    avg_exercise_hours = get_mean(dataframe, "exercise_minutes") / 60  # Convert minutes to hours

    avg_others = 24 - (avg_study_hours + avg_sleep_hours + avg_phone_usage_hours + avg_exercise_hours)

    data = pd.DataFrame({
        "Category": ["Study", "Sleep", "Phone Usage", "Exercise", "Others"],
        "Average Hours": [avg_study_hours, avg_sleep_hours, avg_phone_usage_hours, avg_exercise_hours, avg_others]
    })

    fig = px.pie(data,
                values="Average Hours",
                names="Category",
                title="Average Daily Hours")
    
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(showlegend=True)

    st.plotly_chart(fig, use_container_width=True)

def correlations_study_hours(dataframe: pd.DataFrame):
    st.header("Correlation with Study Hours")
    
    mean_by_age = dataframe.groupby("age")["study_hours_per_day"].mean().reset_index()
    mean_by_gender = dataframe.groupby("gender")["study_hours_per_day"].mean().reset_index()

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(mean_by_age,
            x='age',
            y='study_hours_per_day',
            title="Average Study Hours per Day by Age",)
        fig.update_layout(xaxis_title="Age", yaxis_title="Study Hours per Day")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.bar(mean_by_gender,
            x='gender',
            y='study_hours_per_day',
            title="Average Study Hours per Day by Gender",)
        fig.update_layout(xaxis_title="Gender", yaxis_title="Study Hours per Day")
        st.plotly_chart(fig, use_container_width=True)

def pie_break_hours(dataframe: pd.DataFrame):
    st.header("Average Break Hours per Day")

    avg_breaks = get_mean(dataframe, "breaks_per_day")
    st.subheader(f"Average Breaks per Day: {avg_breaks:.2f}")

    avg_social_media_hours = get_mean(dataframe, "social_media_hours")
    avg_youtube_hours = get_mean(dataframe, "youtube_hours")
    avg_gaming_hours = get_mean(dataframe, "gaming_hours")

    data = pd.DataFrame({
        "Category": ["Social Media", "YouTube", "Gaming"],
        "Average Hours": [avg_social_media_hours, avg_youtube_hours, avg_gaming_hours]
    })

    fig = px.pie(data,
                values="Average Hours",
                names="Category",
                title="Average Break Hours per Day")
    
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(showlegend=True)

    st.plotly_chart(fig, use_container_width=True)

def correlations_breaks(dataframe: pd.DataFrame):
    st.header("Correlation with Breaks per Day")
    
    data = dataframe[["productivity_score", "stress_level", "sleep_hours"]]
    data['total_break_hours'] = dataframe['social_media_hours'] + dataframe['youtube_hours'] + dataframe['gaming_hours']

    avg_productivity_by_breaks = data.groupby("total_break_hours")["productivity_score"].mean().reset_index()
    fig = px.bar(avg_productivity_by_breaks,
            x='total_break_hours',
            y='productivity_score',)
    fig.update_layout(title="Total Break Hours vs Productivity Score",
                    xaxis_title="Youtube + Social Media + Gaming",
                    yaxis_title="Average Productivity Score")
    st.plotly_chart(fig, use_container_width=True)

def correlations_stress(dataframe: pd.DataFrame):
    st.header("Correlations with Stress Level")
    
    data = dataframe[["stress_level", "productivity_score", "assignments_completed", "attendance_percentage"]]

    avg_productivity_by_stress = data.groupby("stress_level")["productivity_score"].mean().reset_index()
    avg_productivity_by_stress['assignments_completed'] = data.groupby("stress_level")["assignments_completed"].mean().reset_index()["assignments_completed"]
    avg_productivity_by_stress['attendance_percentage'] = data.groupby("stress_level")["attendance_percentage"].mean().reset_index()["attendance_percentage"]


    fig = px.bar(avg_productivity_by_stress,
        x='stress_level',
        y='productivity_score',
        color='assignments_completed',
        title="Average Productivity Score by Stress Level with Assignments Completed",)
    fig.update_layout(xaxis_title="Stress Level", yaxis_title="Average Productivity Score", coloraxis_colorbar=dict(title="Assignments Completed"))
    st.plotly_chart(fig, use_container_width=True)

    fig = px.bar(avg_productivity_by_stress,
        x='stress_level',
        y='productivity_score',
        color='attendance_percentage',
        title="Average Productivity Score by Stress Level with Attendance Percentage",)
    fig.update_layout(xaxis_title="Stress Level", yaxis_title="Average Productivity Score", coloraxis_colorbar=dict(title="Attendance Percentage"))
    st.plotly_chart(fig, use_container_width=True)


def analysis(dataframe: pd.DataFrame):
    st.title("Student Productivity Analysis")

    average_scores(dataframe)
    scores_correlation(dataframe)

    correlations_productivity(dataframe)

    pie_daily_hours(dataframe)
    correlations_study_hours(dataframe)
    pie_break_hours(dataframe)

    correlations_breaks(dataframe)
    correlations_stress(dataframe)