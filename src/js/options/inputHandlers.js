export function setUserInputForSubmission(options) {
  const bracketType = options.getCurrentBracketType();
  switch (bracketType) {
    case "artist":
    case "lastfm": {
      const inputValue = document.querySelector("#autoComplete").value.trim();
      options.setInputValue(inputValue);
      break;
    }
    case "battle": {
      const inputValue = document.querySelector("#autoComplete").value.trim();
      options.setInputValue(inputValue);
      const secondaryInputValue = document
        .querySelector("#autoComplete2")
        .value.trim();
      options.setSecondaryInputValue(secondaryInputValue);
      break;
    }
    default:
      return;
  }
}

export function getQueryStringFromUserInput(options) {
  const bracketType = options.getCurrentBracketType();
  const limit = options.getBracketMaxSize();
  switch (bracketType) {
    case "artist":
    case "lastfm": {
      const name = options.getInputValue();
      const queryString = constructQueryString({
        name,
        limit,
      });
      return queryString;
    }
    case "battle": {
      console.log("case battle when handling user input (query string)");
      const name = options.getInputValue();
      const name2 = options.getSecondaryInputValue();
      const queryString = constructQueryString({
        name,
        name2,
        limit,
      });
      return queryString;
    }
    default: {
      const queryString = constructQueryString({
        limit,
      });
      return queryString;
    }
  }
}

function constructQueryString(params) {
  const searchParams = new URLSearchParams();
  for (const prop in params) {
    if (params[prop]) {
      searchParams.append(prop, params[prop]);
    }
  }
  return searchParams;
}
