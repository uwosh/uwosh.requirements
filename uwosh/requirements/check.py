from uwosh.requirements.golivechecks import CHECKS
from zLOG import LOG, WARNING

def get_all():
    checks = []
    
    for klass in CHECKS:
        check = klass()
        if check.use():
            checks.append(check)
    
    return checks

def all_requirements_met(additional_tests=[], or_test=None):
    for check in get_all():
        try:
            if not check.passes():
                if or_test is None or not or_test(check):
                    return False
            
            for additional_test in additional_tests:
                if not additional_test(check):
                    return False
                        
        except Exception, inst:
            LOG("uwosh.requirements", WARNING, "error processing check %s, Exception: %s" % (check.name, inst))
    
    return True
    
def failed():
    failed_checks = []
    
    for check in get_all():
        try:
            if not check.passes():
                failed_checks.append(check)
        except Exception, inst:
            # need to log the error here.
            LOG("uwosh.requirements", WARNING, "error processing check %s, Exception: %s" % (check.name, inst))
            
    return failed_checks