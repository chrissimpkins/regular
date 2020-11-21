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

// Functions
fn re_compile(regex_str: &str) -> PyResult<RegularExpression> {
    match RegularExpression::new(regex_str) {
        Ok(re) => return Ok(re),
        Err(error) => return Err(PyException::new_err(error.to_string())),
    }
}
