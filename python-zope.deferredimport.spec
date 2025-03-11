#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define module	zope.deferredimport
Summary:	Defer Python module import
Summary(pl.UTF-8):	Opóźnianie importu modułów Pythona
Name:		python-%{module}
# keep 4.x here for python2 support
Version:	4.4
Release:	6
License:	ZPL v2.1
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/z/zope.deferredimport/zope.deferredimport-%{version}.tar.gz
# Source0-md5:	05db5a4e2129966e510f9b73368cb7d6
URL:		https://www.zope.dev/
%if %{with python2}
BuildRequires:	python >= 1:2.7
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-zope.proxy
BuildRequires:	python-zope.testrunner
%endif
%endif
%if %{with python3}
BuildRequires:	python3 >= 1:3.5
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-zope.proxy
BuildRequires:	python3-zope.testrunner
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg
%endif
Requires:	python-modules >= 1:2.7
Obsoletes:	Zope-DeferredImport < 3.6.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Defer Python module import.

%description -l pl.UTF-8
Opóźnianie importu modułów Pythona.

%package -n python3-%{module}
Summary:	Defer Python module import
Summary(pl.UTF-8):	Opóźnianie importu modułów Pythona
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-%{module}
Defer Python module import.

%description -n python3-%{module} -l pl.UTF-8
Opóźnianie importu modułów Pythona.

%package apidocs
Summary:	API documentation for Python zope.deferredimport module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona zope.deferredimport
Group:		Documentation

%description apidocs
API documentation for Python zope.deferredimport module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona zope.deferredimport.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
zope-testrunner-2 --test-path=src -v
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
zope-testrunner-3 --test-path=src -v
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/zope/deferredimport/tests.*
%endif

%if %{with python3}
%py3_install

%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/zope/deferredimport/tests.*
%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/zope/deferredimport/__pycache__/tests.*
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst COPYRIGHT.txt LICENSE.txt README.rst
%{py_sitescriptdir}/zope/deferredimport
%{py_sitescriptdir}/zope.deferredimport-*.egg-info
%{py_sitescriptdir}/zope.deferredimport-*-nspkg.pth
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.rst COPYRIGHT.txt LICENSE.txt README.rst
%{py3_sitescriptdir}/zope/deferredimport
%{py3_sitescriptdir}/zope.deferredimport-*.egg-info
%{py3_sitescriptdir}/zope.deferredimport-*-nspkg.pth
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_sources,_static,*.html,*.js}
%endif
