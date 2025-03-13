TOSIGN = ideleg.net nsec3.ideleg.net customer1.ideleg.net customer1.nsec3.ideleg.net customer2.ideleg.net customer2.nsec3.ideleg.net customer3.ideleg.net customer3.nsec3.ideleg.net customer4.ideleg.net deleg.org nsec3.deleg.org customer1.deleg.org customer2.deleg.org customer3.deleg.org customer1.nsec3.deleg.org customer2.nsec3.deleg.org customer3.nsec3.deleg.org
UNSIGNED = customer4.deleg.org customer5.deleg.org customer4.nsec3.deleg.org customer5.nsec3.deleg.org

all: $(TOSIGN:=.signed) $(UNSIGNED)

%: %.in
	./substitute.py $<

ideleg.net.signed: ideleg.net
	ldns-read-zone -psS YYYYMMDDxx `[ -f $@ ] && echo $@ || echo $<` \
	| ldns-signzone -z 1 -f $@.new -o $< - K$<.+013+60397 \
	&& mv $@.new $@

nsec3.ideleg.net.signed: nsec3.ideleg.net
	ldns-read-zone -psS YYYYMMDDxx `[ -f $@ ] && echo $@ || echo $<` \
	| ldns-signzone -n -t 0 -p -z 1 -f $@.new -o $< - K$<.+013+52286 \
	&& mv $@.new $@

customer1.ideleg.net.signed: customer1.ideleg.net
	ldns-read-zone -psS YYYYMMDDxx `[ -f $@ ] && echo $@ || echo $<` \
	| ldns-signzone -z 1 -f $@.new -o $< - K$<.+013+27601 \
	&& mv $@.new $@

customer1.nsec3.ideleg.net.signed: customer1.nsec3.ideleg.net
	ldns-read-zone -psS YYYYMMDDxx `[ -f $@ ] && echo $@ || echo $<` \
	| ldns-signzone -n -t 0 -p -z 1 -f - -o $< - K$<.+013+06616 \
	| ldns-read-zone -u IDELEG > $@.new \
	&& mv $@.new $@

customer2.ideleg.net.signed: customer2.ideleg.net
	ldns-read-zone -psS YYYYMMDDxx `[ -f $@ ] && echo $@ || echo $<` \
	| ldns-signzone -z 1 -f $@.new -o $< - K$<.+013+22597 \
	&& mv $@.new $@

customer2.nsec3.ideleg.net.signed: customer2.nsec3.ideleg.net
	ldns-read-zone -psS YYYYMMDDxx `[ -f $@ ] && echo $@ || echo $<` \
	| ldns-signzone -n -t 0 -p -z 1 -f - -o $< - K$<.+013+39656 \
	| ldns-read-zone -u IDELEG > $@.new \
	&& mv $@.new $@

customer3.ideleg.net.signed: customer3.ideleg.net
	ldns-read-zone -psS YYYYMMDDxx `[ -f $@ ] && echo $@ || echo $<` \
	| ldns-signzone -z 1 -f $@.new -o $< - K$<.+013+62671 \
	&& mv $@.new $@

customer3.nsec3.ideleg.net.signed: customer3.nsec3.ideleg.net
	ldns-read-zone -psS YYYYMMDDxx `[ -f $@ ] && echo $@ || echo $<` \
	| ldns-signzone -n -t 0 -p -z 1 -f $@.new -o $< - K$<.+013+11090 \
	&& mv $@.new $@

customer4.ideleg.net.signed: customer4.ideleg.net
	ldns-read-zone -psS YYYYMMDDxx `[ -f $@ ] && echo $@ || echo $<` \
	| ldns-signzone -z 1 -f $@.new -o $< - K$<.+013+64041 \
	&& mv $@.new $@

customer4.nsec3.ideleg.net.signed: customer4.nsec3.ideleg.net
	ldns-read-zone -psS YYYYMMDDxx `[ -f $@ ] && echo $@ || echo $<` \
	| ldns-signzone -n -t 0 -p -z 1 -f - -o $< - K$<.+013+24809\
	| ldns-read-zone -u IDELEG > $@.new \
	&& mv $@.new $@

deleg.org.signed: deleg.org
	ldns-read-zone -psS YYYYMMDDxx `[ -f $@ ] && echo $@ || echo $<` \
	| ldns-signzone -z 1 -f - -o $< - K$<.+013+15059 \
	| ldns-read-zone -u DELEG > $@.new \
	&& mv $@.new $@

nsec3.deleg.org.signed: nsec3.deleg.org
	ldns-read-zone -psS YYYYMMDDxx `[ -f $@ ] && echo $@ || echo $<` \
	| ldns-signzone -n -t 0 -p -z 1 -f - -o $< - K$<.+013+59425 \
	| ldns-read-zone -u DELEG > $@.new \
	&& mv $@.new $@

customer1.deleg.org.signed: customer1.deleg.org
	ldns-read-zone -psS YYYYMMDDxx `[ -f $@ ] && echo $@ || echo $<` \
	| ldns-signzone -z 1 -f - -o $< - K$<.+013+44593 \
	| ldns-read-zone -u DELEG > $@.new \
	&& mv $@.new $@

customer2.deleg.org.signed: customer2.deleg.org
	ldns-read-zone -psS YYYYMMDDxx `[ -f $@ ] && echo $@ || echo $<` \
	| ldns-signzone -z 1 -f - -o $< - K$<.+013+10829 \
	| ldns-read-zone -u DELEG > $@.new \
	&& mv $@.new $@

customer3.deleg.org.signed: customer3.deleg.org
	ldns-read-zone -psS YYYYMMDDxx `[ -f $@ ] && echo $@ || echo $<` \
	| ldns-signzone -z 1 -f - -o $< - K$<.+013+31173 \
	| ldns-read-zone -u DELEG > $@.new \
	&& mv $@.new $@

customer3.nsec3.deleg.org.signed: customer3.nsec3.deleg.org
	ldns-read-zone -psS YYYYMMDDxx `[ -f $@ ] && echo $@ || echo $<` \
	| ldns-signzone -z 1 -f - -o $< - K$<.+013+46550 \
	| ldns-read-zone -u DELEG > $@.new \
	&& mv $@.new $@

customer2.nsec3.deleg.org.signed: customer2.nsec3.deleg.org
	ldns-read-zone -psS YYYYMMDDxx `[ -f $@ ] && echo $@ || echo $<` \
	| ldns-signzone -z 1 -f - -o $< - K$<.+013+02762 \
	| ldns-read-zone -u DELEG > $@.new \
	&& mv $@.new $@

customer1.nsec3.deleg.org.signed: customer1.nsec3.deleg.org
	ldns-read-zone -psS YYYYMMDDxx `[ -f $@ ] && echo $@ || echo $<` \
	| ldns-signzone -z 1 -f - -o $< - K$<.+013+34489 \
	| ldns-read-zone -u DELEG > $@.new \
	&& mv $@.new $@

sign:
	touch $(TOSIGN)
	$(MAKE)

resign:
	rm -f $(TOSIGN:=.signed)
	$(MAKE) sign

deploy-ideleg: ideleg.net.signed ideleg.net.conf
	scp ideleg.net.signed root@128.199.252.158:/etc/nsd
	scp ideleg.net.conf root@128.199.252.158:/etc/nsd/nsd.conf
	ssh root@128.199.252.158 "nsd-control reconfig || nsd-control start"
	ssh root@128.199.252.158 "nsd-control reload || true"

deploy-supporting: customer1.ideleg.net.signed customer2.ideleg.net.signed customer3.ideleg.net.signed customer4.ideleg.net.signed nsec3.ideleg.net.signed supporting.conf
	scp customer1.ideleg.net.signed root@159.223.42.75:/etc/nsd
	scp customer2.ideleg.net.signed root@159.223.42.75:/etc/nsd
	scp customer3.ideleg.net.signed root@159.223.42.75:/etc/nsd
	scp customer4.ideleg.net.signed root@159.223.42.75:/etc/nsd
	scp nsec3.ideleg.net.signed root@159.223.42.75:/etc/nsd
	scp supporting.conf root@159.223.42.75:/etc/nsd/nsd.conf
	ssh root@159.223.42.75 "nsd-control reconfig || nsd-control start"
	ssh root@159.223.42.75 "nsd-control reload || true"

deploy-nlnetlabs: nlnetlabs.conf customer3.nsec3.ideleg.net.signed
	scp customer3.nsec3.ideleg.net.signed root@152.42.143.10:/etc/nsd
	scp nlnetlabs.conf root@152.42.143.10:/etc/nsd/nsd.conf
	ssh root@152.42.143.10 "nsd-control reconfig || nsd-control start"
	ssh root@152.42.143.10 "nsd-control reload || true"

deploy-legacy: legacy.conf customer1.nsec3.ideleg.net.signed \
		customer2.nsec3.ideleg.net.signed customer4.nsec3.ideleg.net.signed \
		customer1.deleg.org.signed customer2.deleg.org.signed \
		customer3.deleg.org.signed customer3.nsec3.deleg.org.signed \
		customer2.nsec3.deleg.org.signed customer1.nsec3.deleg.org.signed \
		customer4.nsec3.deleg.org customer5.nsec3.deleg.org \
		customer5.deleg.org customer4.deleg.org
	scp customer1.nsec3.ideleg.net.signed root@134.122.39.99:/etc/nsd
	scp customer2.nsec3.ideleg.net.signed root@134.122.39.99:/etc/nsd
	scp customer4.nsec3.ideleg.net.signed root@134.122.39.99:/etc/nsd
	scp customer1.deleg.org.signed root@134.122.39.99:/etc/nsd
	scp customer2.deleg.org.signed root@134.122.39.99:/etc/nsd
	scp customer3.deleg.org.signed root@134.122.39.99:/etc/nsd
	scp customer3.nsec3.deleg.org.signed root@134.122.39.99:/etc/nsd
	scp customer2.nsec3.deleg.org.signed root@134.122.39.99:/etc/nsd
	scp customer1.nsec3.deleg.org.signed root@134.122.39.99:/etc/nsd
	scp customer4.nsec3.deleg.org root@134.122.39.99:/etc/nsd
	scp customer5.nsec3.deleg.org root@134.122.39.99:/etc/nsd
	scp customer5.deleg.org root@134.122.39.99:/etc/nsd
	scp customer4.deleg.org root@134.122.39.99:/etc/nsd
	scp legacy.conf root@134.122.39.99:/etc/nsd/nsd.conf
	ssh root@134.122.39.99 "nsd-control reconfig || nsd-control start"
	ssh root@134.122.39.99 "nsd-control reload || true"

deploy-deleg: deleg.org.conf deleg.org.signed
	scp deleg.org.conf root@146.190.95.45:/etc/nsd/nsd.conf
	scp deleg.org.signed root@146.190.95.45:/etc/nsd
	ssh root@146.190.95.45 "nsd-control reconfig || nsd-control start"
	ssh root@146.190.95.45 "nsd-control reload || true"

deploy-dsupporting: dsupporting.conf nsec3.deleg.org.signed
	scp dsupporting.conf root@178.128.234.33:/etc/nsd/nsd.conf
	scp nsec3.deleg.org.signed root@178.128.234.33:/etc/nsd
	ssh root@178.128.234.33 "nsd-control reconfig || nsd-control start"
	ssh root@178.128.234.33 "nsd-control reload || true"

deploy-dnlnetlabs: dnlnetlabs.conf
	scp dnlnetlabs.conf root@146.190.31.218:/etc/nsd/nsd.conf
	ssh root@146.190.31.218 "nsd-control reconfig || nsd-control start"
	ssh root@146.190.31.218 "nsd-control reload || true"

deploy: deploy-ideleg deploy-supporting deploy-nlnetlabs deploy-legacy \
		deploy-deleg deploy-dsupporting deploy-dnlnetlabs

clean:
	for i in *.in ; do rm -f $${i%.in} $${i%.in}.signed; done
