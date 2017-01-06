#! /usr/bin/env python

def test_func():
    return 0

'''
# 'Otf' below [eg TestOtfSteps]  is 'OpenTaxForms'

from opentaxforms import ut

class TestOtfBase(object):
    def setup_method(self, _):
        dbpath='sqlite:///'+ut.Resource('test','opentaxforms.sqlite3').path()
        self.defaultArgs=dict(
            # skip cleanupFiles to allow comparison with target output
            #skip=['c'],
            dirName='forms',
            # todo change dbpath to dburl
            dbpath=dbpath,
            )
    def teardown_method(self, _):
        pass
    def run(self,**kw):
        rootForms=kw.get('rootForms') or ['1040']
        filesToCheck=kw.get('filesToCheck') or ['f%s-p1.html'%(form,) for form in rootForms]
        kw.update(self.defaultArgs)
        from opentaxforms import opentaxforms as otf
        returnval=otf.opentaxforms(
            okToDownload=False,
            **kw)
        if returnval!=0:
            raise Exception('run failed, no output to compare against target')
        import filecmp
        shallow=False
        outdir,targetdir='forms/','forms-targetOutput/'
        def fmtmsg(result,verb):
            return '{}: output file "{}" in "{}" {} target in "{}"'.format(
                result,fileToCheck,outdir,verb,targetdir)
        for fileToCheck in filesToCheck:
            filesMatch=filecmp.cmp(outdir+fileToCheck,targetdir+fileToCheck,shallow)
            if filesMatch:
                result,verb='PASS','matches'
                print fmtmsg(result,verb)
            else:
                result,verb='FAIL','does NOT match'
                raise Exception(fmtmsg(result,verb))
class TestOtfSteps(TestOtfBase):
    # todo use a less complex form than 1040 to speed testing
    def run_1040_full(self):
        self.run(
            rootForms=['1040'],
            filesToCheck=['f1040-p1.html'],
            )
    def test_run_1040_xfa(self):
        self.run(
            rootForms=['1040'],
            filesToCheck=['f1040-fmt.xml'],
            steps=['x'],
            # speeds testing
            computeOverlap=False,
            )
    # todo add tests of further steps,
    # todo   made fast via pickled results of previous step

class TestOtfApiBase(object):
    def setup_method(self, _):
        from opentaxforms.serve import createApp
        dbpath='sqlite:///'+ut.Resource('test','opentaxforms.sqlite3').path()
        self.app=createApp(dbpath=dbpath)
        self.client=self.app.test_client()
    def teardown_method(self, _):
        pass
class TestOtfApi(TestOtfApiBase):
    def test_api_orgn(self):
        # get list of organizations (currently just IRS)
        response=self.client.get('/api/v1/orgn')
        assert '"code": "us_irs"' in response.data
        assert response.status_code==200
    def test_api_f1040(self):
        # get form 1040
        response=self.client.get('/api/v1/form?q={"filters":[{"name":"code","op":"eq","val":"1040"}]}')
        assert '"title": "Form 1040"' in response.data
        assert response.status_code==200
    def test_api_noresults(self):
        # request a nonexistent form
        response=self.client.get('/api/v1/form?q={"filters":[{"name":"code","op":"eq","val":"0000"}]}')
        assert '"num_results": 0' in response.data
        assert response.status_code==200
    def test_api_filterslots(self):
        # get all checkbox fields on page 1 of form 1040
        import json
        url = '/api/v1/slot?q=%s'
        filters = [
            dict(name='inptyp', op='eq', val='k'),  # inputtype is k for checkbox [vs x for textbox]
            dict(name='page'  , op='eq', val=1),    # on page 1
            dict(name='form', op='has', val=dict(name='code',op='eq',val='1040')),    # of form 1040
            ]
        paramstring = json.dumps(dict(filters=filters))
        response = self.client.get(url%(paramstring,))
        assert response.status_code == 200
        assert '"num_results": 15' in response.data
'''

def main(args):
    def usage():
        print 'usage: "%s" [-h]'%(args[0])
    if len(args)==2:
        if args[1]=='-h':
            usage()
            exit()
        else:
            usage()
    else:
        return test_func()

if __name__=='__main__':
    import sys
    sys.exit(main(sys.argv))

