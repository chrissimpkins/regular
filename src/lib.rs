#![allow(unused)]
// use std::error::Error;

use pyo3::exceptions::PyException;
use pyo3::prelude::*;
use regex::Regex;

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
struct RegularExpression {
    regex: Regex,
}

impl RegularExpression {
    fn new(regex_str: &str) -> Result<Self, regex::Error> {
        match Regex::new(regex_str) {
            Ok(r) => Ok(RegularExpression { regex: r }),
            Err(e) => Err(e),
        }
    }
}

#[pymethods]
impl RegularExpression {
    // auxiliary methods
    pub fn as_str(&self) -> String {
        self.regex.as_str().into()
    }
    // match methods
    pub fn is_match(&self, haystack_str: &str) -> bool {
        self.regex.is_match(haystack_str)
    }

    // replace methods
    pub fn replace(&self, haystack_str: &str, replace_str: &str) -> String {
        self.regex.replace(haystack_str, replace_str).into()
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

// Functions
fn re_compile(regex_str: &str) -> PyResult<RegularExpression> {
    match RegularExpression::new(regex_str) {
        Ok(r) => Ok(r),
        Err(e) => Err(PyException::new_err(e.to_string())),
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
