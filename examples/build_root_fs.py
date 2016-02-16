def build_root_fs( target, source, env ):
   """
   I'm very sorry for this eye bleeding function.
   It's setting up a stack that mounts all the disks, and the directories
   and activates the lvm volumes. And once all that is done then calls
   another function to actually start installing files.
   """
   from plumbum.cmd import mkdir

   target=target[0]

   boot_img = filter( lambda s: str(s).endswith('boot.img'), source )[0]
   root_img = filter( lambda s: str(s).endswith('root.img'), source )[0]
   data_img = filter( lambda s: str(s).endswith('data.img'), source )[0]

   # known order now
   disks = ( boot_img, root_img, data_img )

   with TempDir( prefix='ova_build.' ) as root_dir:
       print "using '%s' as root of new filesystem" % root_dir

       # mount and activate the root lvm
       with losetup(root_img) as root_disk:
           with losetup(root_disk, '-o', 32256 ):
               with vg_activate('amp_sc_root'):
                   src = join('/','dev','amp_sc_root', 'root_lv')
                   with mount(src,root_dir):

                       # mount the boot disk
                       with losetup(boot_img) as boot_disk:
                           with losetup(boot_disk, '-o', 32256 ) as boot_part:
                               boot_dir = join(root_dir,'boot')
                               _cmd( mkdir['-p',boot_dir] )
                               with mount(boot_part,boot_dir):

                                   # mount and activate the data lvm
                                   with losetup(data_img) as data_disk:
                                       with losetup(data_disk, '-o', 32256 ):
                                           with vg_activate('amp_sc_data'):
                                               src = join('/','dev','amp_sc_data', 'data_lv')
                                               data_dir = join(root_dir,'data')
                                               _cmd( mkdir['-p',data_dir] )
                                               with mount(src,data_dir):

                                                   # now start doing the real work
                                                   mk_root_fs( env, disks, root_dir )
