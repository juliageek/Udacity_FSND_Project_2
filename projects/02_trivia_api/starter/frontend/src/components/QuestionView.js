import React, { Component } from 'react';

import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import $ from 'jquery';

import '../stylesheets/QuestionView.css';

class QuestionView extends Component {
  constructor(){
    super();
    this.state = {
      questions: [],
      page: 1,
      totalQuestions: 0,
      categories: [],
      currentCategory: null,
    }
  }

  componentDidMount() {
    this.getQuestions();
  }

  getQuestions = () => {
    $.ajax({
      url: `/questions?page=${this.state.page}`,
      type: "GET",
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          categories: result.categories,
          currentCategory: result.current_category })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  selectPage(num) {
    if (this.state.currentCategory !== undefined) {
    this.setState({page: num}, () => this.getByCategory(this.state.currentCategory.id));
    } else {
      this.setState({page: num}, () => this.getQuestions());
    }
  }

  createPagination(){
    let pageNumbers = [];
    let maxPage = Math.ceil(this.state.totalQuestions / 10)
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <span
          key={i}
          className={`page-num ${i === this.state.page ? 'active' : ''}`}
          onClick={() => {this.selectPage(i)}}>{i}
        </span>)
    }
    return pageNumbers;
  }

  getByCategory=(id) => {
    $.ajax({
      url: `/categories/${id}/questions?page=${this.state.page}`,
      type: "GET",
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category
        })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  submitSearch = (searchTerm) => {
    let url = '/questions';
    if (this.state.currentCategory !== undefined) {
        url = `/categories/${this.state.currentCategory.id}/questions`
    }

    $.ajax({
      url: url,
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({searchTerm: searchTerm}),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions
        })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  questionAction = (id) => (action) => {
    if(action === 'DELETE') {
      if(window.confirm('are you sure you want to delete the question?')) {
        $.ajax({
          url: `/questions/${id}`,
          type: "DELETE",
          success: (result) => {
            if (this.state.currentCategory !== undefined) {
              this.getByCategory(this.state.currentCategory.id);
            } else {
              this.getQuestions();
            }
          },
          error: (error) => {
            alert('Unable to load questions. Please try your request again')
            return;
          }
        })
      }
    }
  }

  render() {
    const questionsLength = this.state.questions.length > 0;
    return (
      <div className="question-view">
        <div className="categories-list">
          <h2 onClick={() => {this.getQuestions()}}>Categories</h2>
          <ul>
            <li
              className="category"
              key="0"
              onClick={() => {this.getQuestions()}}
            >
              All
              <img className="category" src="question.svg"/>
            </li>
              {this.state.categories.map((category) => (
              <li
                className="category"
                key={category.id}
                onClick={() => {this.getByCategory(category.id)}}
              >
                {category.type}
                <img className="category" src={`${category.type.toLowerCase()}.svg`}/>
              </li>
            ))}
          </ul>
          <Search submitSearch={this.submitSearch}/>
        </div>
          <div className="questions-list">
          { questionsLength ? (
              this.state.questions.map((q, ind) => (
                    <Question
                      key={q.id}
                      question={q.question}
                      answer={q.answer}
                      category={this.state.categories[q.category-1]}
                      difficulty={q.difficulty}
                      questionAction={this.questionAction(q.id)}
                    />


              ))
          ) : (
            <div className="no-questions">No questions were found </div>
          )}
          <div className="pagination-menu">
            {this.createPagination()}
          </div>
        </div>
      </div>
    );
  }
}

export default QuestionView;
