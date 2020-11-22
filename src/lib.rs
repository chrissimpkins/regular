#![allow(unused)]
// use std::error::Error;

use pyo3::class::basic::PyObjectProtocol;
use pyo3::exceptions::{PyException, PyValueError};
use pyo3::prelude::*;
use regex::{Regex, RegexBuilder};

#[pymodule]
fn regular(py: Python, m: &PyModule) -> PyResult<()> {
    // Classes
    m.add_class::<RegularExpression>()?;
    // Functions
    #[pyfn(m, "compile")]
    fn compile_py(_py: Python, regex_str: &str) -> PyResult<RegularExpression> {
        re_compile(regex_str)
    }
    Ok(())
}

// Classes
#[pyclass(dict, module = "regular")]
#[derive(Clone, Debug)]
struct RegularExpression {
    regex: Regex,
}

impl RegularExpression {
    fn new(regex_str: &str) -> Result<Self, regex::Error> {
        match RegexBuilder::new(regex_str).build() {
            Ok(r) => Ok(RegularExpression { regex: r }),
            Err(e) => Err(e),
        }
    }
}

#[pyproto]
impl PyObjectProtocol<'_> for RegularExpression {
    fn __repr__(&self) -> PyResult<String> {
        Ok(format!("{:?}", &self)
            .replace("{", "")
            .replace("}", "")
            .replace(" regex:", "with pattern: ")
            .trim()
            .into())
    }

    fn __str__(&self) -> PyResult<String> {
        Ok(format!("{:?}", &self)
            .replace("{", "")
            .replace("}", "")
            .replace(" regex:", "with pattern: ")
            .trim()
            .into())
    }
}

#[pymethods]
impl RegularExpression {
    // auxiliary methods
    pub fn as_str(&self) -> String {
        self.regex.as_str().into()
    }

    // find methods
    pub fn find(&self, haystack_str: &str) -> Option<Match> {
        match self.regex.find(haystack_str) {
            Some(mo) => Some(Match {
                start: mo.start(),
                end: mo.end(),
                range: (mo.range().start, mo.range().end),
                as_str: mo.as_str().into(),
            }),
            None => None,
        }
    }

    // match methods
    pub fn is_match(&self, haystack_str: &str) -> bool {
        self.regex.is_match(haystack_str)
    }

    // replace methods
    pub fn replace(&self, haystack_str: &str, replace_str: &str) -> String {
        self.regex.replace(haystack_str, replace_str).into()
    }

    pub fn replace_all(&self, haystack_str: &str, replace_str: &str) -> String {
        self.regex.replace_all(haystack_str, replace_str).into()
    }

    pub fn replacen(&self, haystack_str: &str, limit: usize, replace_str: &str) -> String {
        self.regex.replacen(haystack_str, limit, replace_str).into()
    }

    // split methods
    // TODO: need to create a split struct and implement the
    // PyIterProtocol trait on it
    // (https://docs.rs/pyo3/0.12.3/pyo3/class/iter/trait.PyIterProtocol.html)

    // pub fn split(&self, haystack_str: &str) -> IterNextOutput<String, &str> {
    //     for x in self.regex.split(haystack_str) {
    //         IterNextOutput::Yield(x.to_string());
    //     }
    //     IterNextOutput::Return("end")
    // }
}

#[pyclass(dict, module = "regular")]
#[derive(Clone, Debug, Eq, PartialEq)]
struct Match {
    #[pyo3(get, set)]
    start: usize,
    #[pyo3(get, set)]
    end: usize,
    #[pyo3(get, set)]
    range: (usize, usize),
    #[pyo3(get, set)]
    as_str: String,
}

// Functions
fn re_compile(regex_str: &str) -> PyResult<RegularExpression> {
    match RegularExpression::new(regex_str) {
        Ok(r) => Ok(r),
        Err(e) => Err(PyValueError::new_err(e.to_string())),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    // RegularExpression struct compile tests
    #[test]
    fn test_regularexpression_compile_success() {
        // should not fail
        assert!(RegularExpression::new("[^01]").is_ok());
    }

    #[test]
    fn test_regularexpression_compile_fail() {
        // should error on invalid regex definition string
        assert!(RegularExpression::new("\\\\\\\\\\\\\\").is_err());
    }
}
