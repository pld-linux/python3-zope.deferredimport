#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define module	zope.deferredimport
Summary:	Defer Python module import
Summary(pl.UTF-8):	Opóźnianie importu modułów Pythona
Name:		python3-%{module}
Version:	5.0
Release:	1
License:	ZPL v2.1
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/z/zope.deferredimport/zope.deferredimport-%{version}.tar.gz
# Source0-md5:	148e4b0fe10b10a40b2abc5b7071c86c
Patch0:		sphinx.patch
URL:		https://www.zope.dev/
BuildRequires:	python3 >= 1:3.7
BuildRequires:	python3-devel >= 1:3.7
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-zope.proxy
BuildRequires:	python3-zope.testrunner
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-repoze.sphinx.autointerface
# already installed package due to package namespace issues (required for "_modules" docs subdir)
BuildRequires:	python3-zope.deferredimport
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Defer Python module import.

%description -l pl.UTF-8
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
%patch -P0 -p1

%build
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
zope-testrunner-3 --test-path=src -v
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/zope/deferredimport/tests.*
%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/zope/deferredimport/__pycache__/tests.*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst COPYRIGHT.txt LICENSE.txt README.rst
%{py3_sitescriptdir}/zope/deferredimport
%{py3_sitescriptdir}/zope.deferredimport-%{version}-py*.egg-info
%{py3_sitescriptdir}/zope.deferredimport-%{version}-py*-nspkg.pth

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,*.html,*.js}
%endif
