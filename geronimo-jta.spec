%global spec_name geronimo-jta_1.1_spec

Name:		geronimo-jta
Version:	1.1.1
Release:	9
Summary:	J2EE JTA v1.1 API

Group:		Development/Java
License:	ASL 2.0
URL:		http://geronimo.apache.org/
# svn export http://svn.apache.org/repos/asf/geronimo/specs/tags/%{spec_name}-%{version}/
Source0:	%{spec_name}-%{version}.tar.bz

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch

# This pulls in almost all of the required java and maven stuff
BuildRequires:	geronimo-parent-poms
BuildRequires:	maven2-plugin-resources

Requires(post):	jpackage-utils
Requires(postun): jpackage-utils

# Ensure a smooth transition from geronimo-specs
Provides:	jta = %{version}-%{release}
Obsoletes:	geronimo-specs <= 1.0-3.3
Obsoletes:	geronimo-specs-compat <= 1.0-3.3

%description
Java Transaction API (JTA) specifies standard Java interfaces between a
transaction manager and the parties involved in a distributed transaction
system: the resource manager, the application server, and the transactional
applications.

%package javadoc
Summary:	API documentation for %{name}
Group:		Development/Java
Requires:	jpackage-utils >= 0:1.7.5
BuildArch:	noarch

%description javadoc
%{summary}.

%prep
%setup -q -n %{spec_name}-%{version}


%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

mvn-jpp \
	-Dmaven.repo.local=$MAVEN_REPO_LOCAL \
	-Dmaven.test.skip=true \
	install javadoc:javadoc


%install
rm -rf $RPM_BUILD_ROOT

install -d -m 755 $RPM_BUILD_ROOT%{_javadir}

install -m 644 target/%{spec_name}-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)
# Also provide compat symlinks
pushd $RPM_BUILD_ROOT%{_javadir} 
ln -sf %{name}-%{version}.jar %{spec_name}-%{version}.jar
ln -sf %{name}-%{version}.jar jta.jar
popd

install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
(cd $RPM_BUILD_ROOT%{_javadocdir} && ln -sf %{name}-%{version} %{name})

install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-%{name}.pom

%add_to_maven_depmap org.apache.geronimo.specs %{spec_name} %{version} JPP %{name}
%add_to_maven_depmap javax.transaction jta %{version} JPP %{name}  

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap

%postun
%update_maven_depmap


%files
%defattr(-,root,root,-)
%doc LICENSE.txt NOTICE.txt
%{_javadir}/*.jar
%{_mavendepmapfragdir}/%{name}
%{_mavenpomdir}/*.pom

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}



