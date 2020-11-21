#![allow(unused)]
// use std::error::Error;

use pyo3::exceptions::PyException;
use pyo3::prelude::*;
use regex::{Error, Regex};

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
