// #![allow(unused)]

use pyo3::class::basic::{CompareOp, PyObjectProtocol};
use pyo3::class::iter::IterNextOutput;
use pyo3::create_exception;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::PyIterProtocol;
use regex::{Regex, RegexBuilder};

// ===================================================
// Module
// ===================================================
#[pymodule]
fn regular(py: Python, m: &PyModule) -> PyResult<()> {
    // Classes
    m.add_class::<Match>()?;
    m.add_class::<MatchesIterator>()?;
    m.add_class::<RegularExpression>()?;
    // Functions
    #[pyfn(m, "compile")]
    fn compile_py(_py: Python, regex_str: &str) -> PyResult<RegularExpression> {
        re_compile(regex_str)
    }
    // Custom exceptions
    m.add(
        "RegularUnimplementedError",
        py.get_type::<RegularUnimplementedError>(),
    )?;
    Ok(())
}

// ===================================================
// Classes
// ===================================================
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
    // protocol methods documented in https://pyo3.rs/master/class/protocols.html
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

    fn __richcmp__(&self, other: RegularExpression, op: CompareOp) -> PyResult<bool> {
        match op {
            CompareOp::Eq => Ok(self.regex.as_str() == other.regex.as_str()),
            CompareOp::Ne => Ok(self.regex.as_str() != other.regex.as_str()),
            _ => Err(RegularUnimplementedError::new_err(
                "unimplemented comparison operator",
            )),
        }
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
                text: mo.as_str().into(),
            }),
            None => None,
        }
    }

    pub fn find_all(&self, haystack_str: &str) -> Vec<Match> {
        self.regex
            .find_iter(haystack_str)
            .map(|m| Match {
                start: m.start(),
                end: m.end(),
                text: m.as_str().into(),
            })
            .collect()
    }

    pub fn find_iter(&self, haystack_str: &str) -> MatchesIterator {
        MatchesIterator {
            iterator: std::boxed::Box::new(self.find_all(haystack_str).into_iter()),
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

    pub fn split<'t>(&self, haystack_str: &'t str) -> Vec<&'t str> {
        self.regex.split(haystack_str).collect()
    }

    pub fn splitn<'t>(&self, haystack_str: &'t str, limit: usize) -> Vec<&'t str> {
        self.regex.splitn(haystack_str, limit).collect()
    }
}

#[pyclass(dict, module = "regular")]
#[derive(Clone, Debug, Eq, PartialEq)]
struct Match {
    #[pyo3(get, set)]
    start: usize,
    #[pyo3(get, set)]
    end: usize,
    #[pyo3(get, set)]
    text: String,
}

#[pymethods]
impl Match {
    pub fn as_str(&self) -> &str {
        &self.text
    }

    pub fn range(&self) -> (usize, usize) {
        (self.start, self.end)
    }
}

#[pyproto]
impl PyObjectProtocol<'_> for Match {
    // protocol methods documented in https://pyo3.rs/master/class/protocols.html
    fn __repr__(&self) -> PyResult<String> {
        Ok(format!("{:?}", &self)
            .replace("{", "<")
            .replace("}", ">")
            .trim()
            .into())
    }

    fn __str__(&self) -> PyResult<String> {
        Ok(format!("{:?}", &self)
            .replace("{", "<")
            .replace("}", ">")
            .trim()
            .into())
    }

    fn __richcmp__(&self, other: Match, op: CompareOp) -> PyResult<bool> {
        match op {
            CompareOp::Eq => Ok(self == &other),
            CompareOp::Ne => Ok(self != &other),
            _ => Err(RegularUnimplementedError::new_err(
                "unimplemented comparison operator",
            )),
        }
    }
}

#[pyclass(dict, module = "regular")]
struct MatchesIterator {
    iterator: Box<dyn Iterator<Item = Match> + Send>,
}

#[pyproto]
impl PyIterProtocol for MatchesIterator {
    fn __iter__(slf: PyRef<Self>) -> PyRef<Self> {
        slf
    }

    fn __next__(mut slf: PyRefMut<Self>) -> IterNextOutput<Match, &'static str> {
        match slf.iterator.next() {
            Some(mo) => IterNextOutput::Yield(mo),
            None => IterNextOutput::Return("Ended"),
        }
    }
}

// ===================================================
// Functions
// ===================================================
fn re_compile(regex_str: &str) -> PyResult<RegularExpression> {
    match RegularExpression::new(regex_str) {
        Ok(r) => Ok(r),
        Err(e) => Err(PyValueError::new_err(e.to_string())),
    }
}

// ===================================================
// Exceptions
// ===================================================
create_exception!(
    regular,
    RegularUnimplementedError,
    pyo3::exceptions::PyException
);

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
